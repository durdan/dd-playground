from typing import List, Dict, Set
from test_coordinator import TestResult, TestType
import hashlib

class TestAggregator:
    def aggregate_results(self, results: List[TestResult]) -> Dict[str, List[TestResult]]:
        """Aggregate and deduplicate test results."""
        if not results:
            return {}
        
        # Group by test type
        grouped = self._group_by_test_type(results)
        
        # Deduplicate within each group
        deduplicated = {}
        for test_type, test_results in grouped.items():
            deduplicated[test_type] = self._deduplicate_tests(test_results)
        
        return deduplicated

    def _group_by_test_type(self, results: List[TestResult]) -> Dict[str, List[TestResult]]:
        """Group results by test type."""
        grouped = {}
        for result in results:
            test_type_key = result.test_type.value
            if test_type_key not in grouped:
                grouped[test_type_key] = []
            grouped[test_type_key].append(result)
        return grouped

    def _deduplicate_tests(self, results: List[TestResult]) -> List[TestResult]:
        """Remove duplicate test results based on content similarity."""
        if len(results) <= 1:
            return results
        
        seen_hashes: Set[str] = set()
        unique_results = []
        
        for result in results:
            content_hash = self._hash_test_content(result.test_code)
            if content_hash not in seen_hashes:
                seen_hashes.add(content_hash)
                unique_results.append(result)
        
        # If we have multiple unique results, prefer successful ones
        if len(unique_results) > 1:
            successful_results = [r for r in unique_results if r.success]
            if successful_results:
                # Return the one with highest coverage
                return [max(successful_results, key=lambda r: r.coverage_info.get('estimated_coverage', 0))]
        
        return unique_results

    def _hash_test_content(self, test_code: str) -> str:
        """Create hash of test content for deduplication."""
        # Normalize whitespace and remove comments for better deduplication
        normalized = ' '.join(test_code.split())
        return hashlib.md5(normalized.encode()).hexdigest()