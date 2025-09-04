from typing import List, Optional, Callable
from datetime import datetime, timedelta
import time
from models import Repository, Phase, RolloutState, RolloutStatus
from strategies import RolloutStrategy, PilotFirstStrategy
from rollout_tracker import RolloutTracker
from validation_service import ValidationService

class RolloutManager:
    def __init__(self, 
                 repositories: List[Repository],
                 phases: List[Phase],
                 strategy: RolloutStrategy = None,
                 tracker: RolloutTracker = None):
        
        # Validate inputs
        repo_errors = ValidationService.validate_repositories(repositories)
        phase_errors = ValidationService.validate_phases(phases)
        
        if repo_errors or phase_errors:
            all_errors = repo_errors + phase_errors
            raise ValueError(f"Validation failed: {'; '.join(all_errors)}")
        
        self.repositories = repositories
        self.phases = phases
        self.strategy = strategy or PilotFirstStrategy()
        self.tracker = tracker or RolloutTracker()
    
    def start_rollout(self, rollout_id: str) -> RolloutState:
        if self.tracker.get_state(rollout_id):
            raise ValueError(f"Rollout {rollout_id} already exists")
        
        state = RolloutState(
            rollout_id=rollout_id,
            current_phase=0,
            status=RolloutStatus.PENDING
        )
        
        self.tracker.update_state(state)
        return state
    
    def execute_phase(self, rollout_id: str, 
                     deploy_fn: Callable[[Repository], bool]) -> bool:
        state = self.tracker.get_state(rollout_id)
        if not state:
            raise ValueError(f"Rollout {rollout_id} not found")
        
        if state.current_phase >= len(self.phases):
            state.status = RolloutStatus.COMPLETED
            self.tracker.update_state(state)
            return True
        
        phase = self.phases[state.current_phase]
        
        # Check if we need to wait
        if state.phase_start_time:
            wait_until = state.phase_start_time + timedelta(hours=phase.wait_time_hours)
            if datetime.now() < wait_until:
                return False
        
        # Calculate target repositories for this phase
        total_repos = len(self.repositories)
        target_count = int((phase.target_percentage / 100) * total_repos)
        
        # Select repositories to deploy
        candidates = self.strategy.select_repositories(
            self.repositories, 
            target_count, 
            state.deployed_repos | state.failed_repos
        )
        
        if not candidates:
            # No more repositories to deploy, move to next phase
            return self._advance_phase(state)
        
        # Execute deployments
        state.status = RolloutStatus.IN_PROGRESS
        if not state.phase_start_time:
            state.phase_start_time = datetime.now()
        
        success_count = 0
        for repo in candidates:
            try:
                if deploy_fn(repo):
                    state.deployed_repos.add(repo.name)
                    success_count += 1
                else:
                    state.failed_repos.add(repo.name)
            except Exception:
                state.failed_repos.add(repo.name)
        
        # Check phase completion criteria
        total_deployed = len(state.deployed_repos)
        success_rate = success_count / len(candidates) if candidates else 0
        
        if len(state.failed_repos) > phase.max_failures:
            state.status = RolloutStatus.FAILED
            self.tracker.update_state(state)
            return False
        
        if success_rate < phase.min_success_rate:
            state.status = RolloutStatus.PAUSED
            self.tracker.update_state(state)
            return False
        
        self.tracker.update_state(state)
        
        # Check if phase is complete
        phase_target = int((phase.target_percentage / 100) * total_repos)
        if total_deployed >= phase_target:
            return self._advance_phase(state)
        
        return True
    
    def _advance_phase(self, state: RolloutState) -> bool:
        state.current_phase += 1
        state.phase_start_time = None
        
        if state.current_phase >= len(self.phases):
            state.status = RolloutStatus.COMPLETED
        else:
            state.status = RolloutStatus.PENDING
        
        self.tracker.update_state(state)
        return state.status == RolloutStatus.COMPLETED
    
    def get_rollout_status(self, rollout_id: str) -> Optional[RolloutState]:
        return self.tracker.get_state(rollout_id)
    
    def pause_rollout(self, rollout_id: str):
        state = self.tracker.get_state(rollout_id)
        if state:
            state.status = RolloutStatus.PAUSED
            self.tracker.update_state(state)
    
    def resume_rollout(self, rollout_id: str):
        state = self.tracker.get_state(rollout_id)
        if state and state.status == RolloutStatus.PAUSED:
            state.status = RolloutStatus.PENDING
            self.tracker.update_state(state)