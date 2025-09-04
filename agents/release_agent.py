"""Release Prep Agent - Orchestrates release preparation workflow."""

import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime

from .pr_agent import PRAgent
from .audit_agent import AuditAgent  
from .plans_agent import PlansAgent

logger = logging.getLogger(__name__)


@dataclass
class ReleaseConfig:
    """Configuration for release preparation."""
    version: str
    branch: str = "main"
    require_all_prs_merged: bool = True
    require_audit_pass: bool = True
    require_plans_validated: bool = True
    min_test_coverage: float = 0.8
    changelog_path: str = "CHANGELOG.md"


@dataclass
class ReleaseStatus:
    """Status of release preparation."""
    ready: bool
    version: str
    checks_passed: List[str]
    checks_failed: List[str]
    warnings: List[str]
    timestamp: datetime


class ReleaseValidator:
    """Validates release readiness across different systems."""
    
    def __init__(self, pr_agent: PRAgent, audit_agent: AuditAgent, plans_agent: PlansAgent):
        self.pr_agent = pr_agent
        self.audit_agent = audit_agent
        self.plans_agent = plans_agent
    
    def validate_prs(self, config: ReleaseConfig) -> Dict[str, Any]:
        """Validate PR status for release."""
        try:
            pr_status = self.pr_agent.get_branch_status(config.branch)
            
            open_prs = [pr for pr in pr_status.get('prs', []) if pr.get('state') == 'open']
            
            if config.require_all_prs_merged and open_prs:
                return {
                    'passed': False,
                    'message': f"Found {len(open_prs)} open PRs that need to be merged",
                    'details': open_prs
                }
            
            return {
                'passed': True,
                'message': "All PRs are properly merged",
                'details': pr_status
            }
            
        except Exception as e:
            logger.error(f"PR validation failed: {e}")
            return {
                'passed': False,
                'message': f"PR validation error: {str(e)}",
                'details': {}
            }
    
    def validate_audits(self, config: ReleaseConfig) -> Dict[str, Any]:
        """Validate audit status for release."""
        try:
            audit_result = self.audit_agent.run_full_audit()
            
            if config.require_audit_pass and not audit_result.get('passed', False):
                return {
                    'passed': False,
                    'message': "Audit checks failed",
                    'details': audit_result
                }
            
            return {
                'passed': True,
                'message': "All audit checks passed",
                'details': audit_result
            }
            
        except Exception as e:
            logger.error(f"Audit validation failed: {e}")
            return {
                'passed': False,
                'message': f"Audit validation error: {str(e)}",
                'details': {}
            }
    
    def validate_plans(self, config: ReleaseConfig) -> Dict[str, Any]:
        """Validate plans for release."""
        try:
            plans_status = self.plans_agent.validate_all_plans()
            
            if config.require_plans_validated and not plans_status.get('valid', False):
                return {
                    'passed': False,
                    'message': "Plan validation failed",
                    'details': plans_status
                }
            
            return {
                'passed': True,
                'message': "All plans validated successfully",
                'details': plans_status
            }
            
        except Exception as e:
            logger.error(f"Plans validation failed: {e}")
            return {
                'passed': False,
                'message': f"Plans validation error: {str(e)}",
                'details': {}
            }


class ReleasePrep:
    """Core release preparation logic."""
    
    def __init__(self, validator: ReleaseValidator):
        self.validator = validator
    
    def prepare_release(self, config: ReleaseConfig) -> ReleaseStatus:
        """Prepare release by running all validation checks."""
        logger.info(f"Starting release preparation for version {config.version}")
        
        checks_passed = []
        checks_failed = []
        warnings = []
        
        # Validate PRs
        pr_result = self.validator.validate_prs(config)
        if pr_result['passed']:
            checks_passed.append("PR validation")
        else:
            checks_failed.append(f"PR validation: {pr_result['message']}")
        
        # Validate audits
        audit_result = self.validator.validate_audits(config)
        if audit_result['passed']:
            checks_passed.append("Audit validation")
        else:
            checks_failed.append(f"Audit validation: {audit_result['message']}")
        
        # Validate plans
        plans_result = self.validator.validate_plans(config)
        if plans_result['passed']:
            checks_passed.append("Plans validation")
        else:
            checks_failed.append(f"Plans validation: {plans_result['message']}")
        
        # Generate changelog
        try:
            self._update_changelog(config)
            checks_passed.append("Changelog updated")
        except Exception as e:
            warnings.append(f"Changelog update failed: {str(e)}")
        
        ready = len(checks_failed) == 0
        
        return ReleaseStatus(
            ready=ready,
            version=config.version,
            checks_passed=checks_passed,
            checks_failed=checks_failed,
            warnings=warnings,
            timestamp=datetime.now()
        )
    
    def _update_changelog(self, config: ReleaseConfig) -> None:
        """Update changelog with release information."""
        try:
            with open(config.changelog_path, 'r') as f:
                content = f.read()
            
            # Simple changelog update - prepend new version
            new_entry = f"\n## [{config.version}] - {datetime.now().strftime('%Y-%m-%d')}\n\n"
            
            # Insert after first line (assuming it's a title)
            lines = content.split('\n')
            if lines:
                lines.insert(1, new_entry)
                
            with open(config.changelog_path, 'w') as f:
                f.write('\n'.join(lines))
                
        except FileNotFoundError:
            # Create new changelog
            with open(config.changelog_path, 'w') as f:
                f.write(f"# Changelog\n\n## [{config.version}] - {datetime.now().strftime('%Y-%m-%d')}\n\n")


class ReleaseNotifier:
    """Handles release notifications."""
    
    def notify_release_status(self, status: ReleaseStatus) -> None:
        """Send notification about release status."""
        if status.ready:
            logger.info(f"✅ Release {status.version} is ready!")
            logger.info(f"Passed checks: {', '.join(status.checks_passed)}")
        else:
            logger.warning(f"❌ Release {status.version} is NOT ready")
            logger.warning(f"Failed checks: {', '.join(status.checks_failed)}")
        
        if status.warnings:
            logger.warning(f"Warnings: {', '.join(status.warnings)}")


class ReleaseAgent:
    """Main Release Prep Agent."""
    
    def __init__(self, pr_agent: PRAgent, audit_agent: AuditAgent, plans_agent: PlansAgent):
        self.validator = ReleaseValidator(pr_agent, audit_agent, plans_agent)
        self.release_prep = ReleasePrep(self.validator)
        self.notifier = ReleaseNotifier()
    
    def prepare_release(self, version: str, **kwargs) -> ReleaseStatus:
        """Main entry point for release preparation."""
        if not version:
            raise ValueError("Version is required for release preparation")
        
        config = ReleaseConfig(version=version, **kwargs)
        status = self.release_prep.prepare_release(config)
        self.notifier.notify_release_status(status)
        
        return status
    
    def check_release_readiness(self, version: str, **kwargs) -> bool:
        """Quick check if release is ready."""
        status = self.prepare_release(version, **kwargs)
        return status.ready