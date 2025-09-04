from typing import List, Dict
from datetime import datetime
import uuid
import logging

from models.security_report import SecurityReport, ScanResult
from services.docker_manager import DockerManager
from services.security_tools import TrivyScanner, GitLeaksScanner, DockerBenchScanner

logger = logging.getLogger(__name__)

class DockerSecurityScanner:
    def __init__(self):
        self.docker_manager = DockerManager()
        self.scanners = {
            'trivy': TrivyScanner(self.docker_manager),
            'gitleaks': GitLeaksScanner(self.docker_manager),
            'docker-bench': DockerBenchScanner(self.docker_manager)
        }
    
    def run_scan(self, target: str, scan_types: List[str] = None) -> SecurityReport:
        """Run security scans on target"""
        if not scan_types:
            scan_types = list(self.scanners.keys())
        
        scan_id = str(uuid.uuid4())
        scan_results = []
        
        logger.info(f"Starting security scan {scan_id} for target: {target}")
        
        for scan_type in scan_types:
            if scan_type not in self.scanners:
                logger.warning(f"Unknown scan type: {scan_type}")
                continue
            
            try:
                logger.info(f"Running {scan_type} scan...")
                result = self.scanners[scan_type].scan(target)
                scan_results.append(result)
                logger.info(f"{scan_type} scan completed with {len(result.findings)} findings")
            except Exception as e:
                logger.error(f"Failed to run {scan_type} scan: {e}")
        
        overall_summary = self._generate_overall_summary(scan_results)
        recommendations = self._generate_recommendations(scan_results)
        
        report = SecurityReport(
            scan_id=scan_id,
            target=target,
            timestamp=datetime.now(),
            scan_results=scan_results,
            overall_summary=overall_summary,
            recommendations=recommendations
        )
        
        logger.info(f"Security scan {scan_id} completed")
        return report
    
    def _generate_overall_summary(self, scan_results: List[ScanResult]) -> Dict[str, int]:
        """Aggregate findings across all scans"""
        overall = {"critical": 0, "high": 0, "medium": 0, "low": 0, "info": 0}
        
        for result in scan_results:
            for severity, count in result.summary.items():
                overall[severity] += count
        
        return overall
    
    def _generate_recommendations(self, scan_results: List[ScanResult]) -> List[str]:
        """Generate security recommendations based on findings"""
        recommendations = []
        
        for result in scan_results:
            if result.summary.get("critical", 0) > 0:
                recommendations.append(f"Address {result.summary['critical']} critical issues found by {result.tool_name}")
            
            if result.summary.get("high", 0) > 0:
                recommendations.append(f"Review {result.summary['high']} high-severity findings from {result.tool_name}")
        
        if not recommendations:
            recommendations.append("No critical security issues found. Continue monitoring.")
        
        return recommendations