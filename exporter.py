import csv
import json
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path
from typing import List, Iterator
from models import LogEntry, ExportFormat

class ComplianceExporter:
    def __init__(self):
        pass
    
    def export_logs(self, logs: Iterator[LogEntry], output_path: str, 
                   format: ExportFormat) -> str:
        """Export logs to specified format and return the file path."""
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        if format == ExportFormat.JSON:
            return self._export_json(logs, output_file)
        elif format == ExportFormat.CSV:
            return self._export_csv(logs, output_file)
        elif format == ExportFormat.XML:
            return self._export_xml(logs, output_file)
        else:
            raise ValueError(f"Unsupported export format: {format}")
    
    def _export_json(self, logs: Iterator[LogEntry], output_file: Path) -> str:
        """Export logs as JSON array."""
        log_list = [log.to_dict() for log in logs]
        
        export_data = {
            "export_timestamp": datetime.now().isoformat(),
            "total_entries": len(log_list),
            "logs": log_list
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)
        
        return str(output_file)
    
    def _export_csv(self, logs: Iterator[LogEntry], output_file: Path) -> str:
        """Export logs as CSV."""
        log_list = list(logs)
        
        if not log_list:
            # Create empty CSV with headers
            with open(output_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['timestamp', 'level', 'message', 'crew_id', 
                               'agent_id', 'task_id', 'metadata'])
            return str(output_file)
        
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=[
                'timestamp', 'level', 'message', 'crew_id', 
                'agent_id', 'task_id', 'metadata'
            ])
            writer.writeheader()
            
            for log in log_list:
                row = log.to_dict()
                # Convert metadata dict to JSON string for CSV
                if row['metadata']:
                    row['metadata'] = json.dumps(row['metadata'])
                writer.writerow(row)
        
        return str(output_file)
    
    def _export_xml(self, logs: Iterator[LogEntry], output_file: Path) -> str:
        """Export logs as XML."""
        root = ET.Element("compliance_export")
        root.set("export_timestamp", datetime.now().isoformat())
        
        logs_element = ET.SubElement(root, "logs")
        entry_count = 0
        
        for log in logs:
            log_element = ET.SubElement(logs_element, "log_entry")
            
            for key, value in log.to_dict().items():
                if value is not None:
                    elem = ET.SubElement(log_element, key)
                    if isinstance(value, dict):
                        elem.text = json.dumps(value)
                    else:
                        elem.text = str(value)
            
            entry_count += 1
        
        root.set("total_entries", str(entry_count))
        
        tree = ET.ElementTree(root)
        tree.write(output_file, encoding='utf-8', xml_declaration=True)
        
        return str(output_file)