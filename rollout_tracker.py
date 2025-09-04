from typing import Dict, Optional
import json
from datetime import datetime
from models import RolloutState, RolloutStatus

class RolloutTracker:
    def __init__(self, storage_path: str = "rollout_state.json"):
        self.storage_path = storage_path
        self._states: Dict[str, RolloutState] = {}
        self._load_state()
    
    def _load_state(self):
        try:
            with open(self.storage_path, 'r') as f:
                data = json.load(f)
                for rollout_id, state_data in data.items():
                    state = RolloutState(
                        rollout_id=state_data['rollout_id'],
                        current_phase=state_data['current_phase'],
                        status=RolloutStatus(state_data['status']),
                        deployed_repos=set(state_data['deployed_repos']),
                        failed_repos=set(state_data['failed_repos']),
                        phase_start_time=datetime.fromisoformat(state_data['phase_start_time']) 
                                        if state_data.get('phase_start_time') else None,
                        created_at=datetime.fromisoformat(state_data['created_at'])
                    )
                    self._states[rollout_id] = state
        except FileNotFoundError:
            pass
    
    def _save_state(self):
        data = {}
        for rollout_id, state in self._states.items():
            data[rollout_id] = {
                'rollout_id': state.rollout_id,
                'current_phase': state.current_phase,
                'status': state.status.value,
                'deployed_repos': list(state.deployed_repos),
                'failed_repos': list(state.failed_repos),
                'phase_start_time': state.phase_start_time.isoformat() if state.phase_start_time else None,
                'created_at': state.created_at.isoformat()
            }
        
        with open(self.storage_path, 'w') as f:
            json.dump(data, f, indent=2)
    
    def get_state(self, rollout_id: str) -> Optional[RolloutState]:
        return self._states.get(rollout_id)
    
    def update_state(self, state: RolloutState):
        self._states[state.rollout_id] = state
        self._save_state()
    
    def delete_state(self, rollout_id: str):
        if rollout_id in self._states:
            del self._states[rollout_id]
            self._save_state()