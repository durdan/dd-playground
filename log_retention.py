import os
import json
from datetime import datetime, timedelta
from typing import List, Dict
from models import RetentionPolicy

class LogRetentionManager:
    def __init__(self, storage_path: str = "logs"):
        self.storage_path = storage_path
        self.policies: Dict[str, RetentionPolicy] = {}
        self._ensure_storage_exists()
    
    def _ensure_storage_exists(self):
        os.makedirs(self.storage_path, exist_ok=True)
    
    def add_retention_policy(self, policy: RetentionPolicy):
        if policy.retention_days <= 0:
            raise ValueError("Retention days must be positive")
        self.policies[policy.log_type] = policy
    
    def store_log(self, log_type: str, log_data: Dict):
        if not log_type or not log_data:
            raise ValueError("Log type and data are required")
        
        timestamp = datetime.now().isoformat()
        log_entry = {
            "timestamp": timestamp,
            "type": log_type,
            "data": log_data
        }
        
        log_file = os.path.join(self.storage_path, f"{log_type}_{datetime.now().strftime('%Y%m%d')}.json")
        
        # Append to daily log file
        logs = []
        if os.path.exists(log_file):
            with open(log_file, 'r') as f:
                logs = json.load(f)
        
        logs.append(log_entry)
        
        with open(log_file, 'w') as f:
            json.dump(logs, f, indent=2)
    
    def cleanup_expired_logs(self) -> Dict[str, int]:
        if not self.policies:
            return {}
        
        cleanup_results = {}
        current_time = datetime.now()
        
        for log_type, policy in self.policies.items():
            deleted_count = 0
            cutoff_date = current_time - timedelta(days=policy.retention_days)
            
            # Find and process log files for this type
            for filename in os.listdir(self.storage_path):
                if filename.startswith(f"{log_type}_") and filename.endswith('.json'):
                    file_path = os.path.join(self.storage_path, filename)
                    
                    try:
                        with open(file_path, 'r') as f:
                            logs = json.load(f)
                        
                        # Filter out expired logs
                        filtered_logs = []
                        for log in logs:
                            log_time = datetime.fromisoformat(log['timestamp'])
                            if log_time >= cutoff_date:
                                filtered_logs.append(log)
                            else:
                                deleted_count += 1
                        
                        # Update file or delete if empty
                        if filtered_logs:
                            with open(file_path, 'w') as f:
                                json.dump(filtered_logs, f, indent=2)
                        elif policy.auto_delete:
                            os.remove(file_path)
                    
                    except (json.JSONDecodeError, KeyError, ValueError):
                        continue  # Skip corrupted files
            
            cleanup_results[log_type] = deleted_count
        
        return cleanup_results
    
    def get_logs(self, log_type: str, days_back: int = 7) -> List[Dict]:
        if days_back <= 0:
            raise ValueError("Days back must be positive")
        
        logs = []
        cutoff_date = datetime.now() - timedelta(days=days_back)
        
        for filename in os.listdir(self.storage_path):
            if filename.startswith(f"{log_type}_") and filename.endswith('.json'):
                file_path = os.path.join(self.storage_path, filename)
                
                try:
                    with open(file_path, 'r') as f:
                        file_logs = json.load(f)
                    
                    for log in file_logs:
                        log_time = datetime.fromisoformat(log['timestamp'])
                        if log_time >= cutoff_date:
                            logs.append(log)
                
                except (json.JSONDecodeError, KeyError, ValueError):
                    continue
        
        return sorted(logs, key=lambda x: x['timestamp'])