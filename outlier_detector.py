from typing import List
from models import MetricData, OutlierResult
import statistics

class OutlierDetector:
    
    def detect_outliers(self, data: List[MetricData]) -> List[OutlierResult]:
        """Detect outliers using IQR method, grouped by metric."""
        outlier_results = []
        grouped_data = self._group_by_metric_with_dates(data)
        
        for metric_name, metric_data in grouped_data.items():
            values = [item['value'] for item in metric_data]
            
            if len(values) < 4:  # Need at least 4 points for IQR
                continue
                
            outliers = self._find_outliers_iqr(values)
            if outliers:
                outlier_dates = [
                    item['date'] for item in metric_data 
                    if item['value'] in outliers
                ]
                
                q1 = statistics.quantiles(values, n=4)[0]
                q3 = statistics.quantiles(values, n=4)[2]
                iqr = q3 - q1
                
                outlier_results.append(OutlierResult(
                    metric_name=metric_name,
                    outlier_values=outliers,
                    outlier_dates=outlier_dates,
                    threshold_lower=q1 - 1.5 * iqr,
                    threshold_upper=q3 + 1.5 * iqr
                ))
        
        return outlier_results
    
    def _group_by_metric_with_dates(self, data: List[MetricData]) -> dict:
        """Group data by metric name, preserving dates."""
        grouped = {}
        for item in data:
            if item.metric_name not in grouped:
                grouped[item.metric_name] = []
            grouped[item.metric_name].append({
                'date': item.date,
                'value': item.value
            })
        return grouped
    
    def _find_outliers_iqr(self, values: List[float]) -> List[float]:
        """Find outliers using Interquartile Range method."""
        if len(values) < 4:
            return []
            
        q1 = statistics.quantiles(values, n=4)[0]
        q3 = statistics.quantiles(values, n=4)[2]
        iqr = q3 - q1
        
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr
        
        return [v for v in values if v < lower_bound or v > upper_bound]