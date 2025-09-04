import json
from datetime import datetime, timedelta
from typing import Dict, List, Tuple
from dataclasses import dataclass

@dataclass
class ReviewResult:
    model_name: str
    version: str
    performance_score: float
    threshold: float
    passed: bool
    recommendations: List[str]
    review_date: str

class MonthlyReviewService:
    def __init__(self, model_manager, config_manager):
        self.model_manager = model_manager
        self.config_manager = config_manager
        self.reviews_path = "/data/reviews"
        self._ensure_directory()
    
    def _ensure_directory(self):
        import os
        os.makedirs(self.reviews_path, exist_ok=True)
    
    def conduct_review(self, model_name: str) -> ReviewResult:
        """Conduct monthly review for a specific model"""
        active_version = self.model_manager.get_active_version(model_name)
        if not active_version:
            raise ValueError(f"No active version found for model {model_name}")
        
        # Get model configuration
        model_config = next(
            (m for m in self.config_manager.models if m.name == model_name),
            None
        )
        if not model_config:
            raise ValueError(f"No configuration found for model {model_name}")
        
        # Simulate performance evaluation (in production, use real metrics)
        performance_score = self._evaluate_model_performance(model_name, active_version)
        
        passed = performance_score >= model_config.performance_threshold
        recommendations = self._generate_recommendations(
            model_name, performance_score, model_config.performance_threshold
        )
        
        result = ReviewResult(
            model_name=model_name,
            version=active_version,
            performance_score=performance_score,
            threshold=model_config.performance_threshold,
            passed=passed,
            recommendations=recommendations,
            review_date=datetime.now().isoformat()
        )
        
        self._save_review_result(result)
        return result
    
    def _evaluate_model_performance(self, model_name: str, version: str) -> float:
        """Evaluate model performance (mock implementation)"""
        # In production, this would:
        # 1. Load test dataset
        # 2. Run model inference
        # 3. Calculate metrics (accuracy, F1, etc.)
        # 4. Return aggregated score
        
        # Mock performance based on model name hash for consistency
        import hashlib
        hash_val = int(hashlib.md5(f"{model_name}{version}".encode()).hexdigest()[:8], 16)
        return 0.7 + (hash_val % 30) / 100  # Returns value between 0.7-0.99
    
    def _generate_recommendations(self, model_name: str, score: float, 
                                threshold: float) -> List[str]:
        """Generate recommendations based on performance"""
        recommendations = []
        
        if score < threshold:
            recommendations.append("Performance below threshold - consider retraining")
            recommendations.append("Review training data for quality issues")
            recommendations.append("Analyze feature importance and model architecture")
        
        if score < threshold * 0.9:
            recommendations.append("URGENT: Consider immediate rollback to previous version")
        
        if score >= threshold:
            recommendations.append("Performance meets requirements")
            if score > threshold * 1.1:
                recommendations.append("Excellent performance - consider as baseline")
        
        return recommendations
    
    def _save_review_result(self, result: ReviewResult):
        """Save review result to file"""
        filename = f"{result.model_name}_{result.review_date[:10]}.json"
        filepath = f"{self.reviews_path}/{filename}"
        
        with open(filepath, 'w') as f:
            json.dump(result.__dict__, f, indent=2)
    
    def conduct_all_reviews(self) -> List[ReviewResult]:
        """Conduct reviews for all configured models"""
        results = []
        for model_config in self.config_manager.models:
            try:
                result = self.conduct_review(model_config.name)
                results.append(result)
            except Exception as e:
                print(f"Failed to review {model_config.name}: {e}")
        
        return results
    
    def get_review_history(self, model_name: str, days: int = 90) -> List[Dict]:
        """Get review history for a model"""
        import os
        import glob
        
        pattern = f"{self.reviews_path}/{model_name}_*.json"
        review_files = glob.glob(pattern)
        
        cutoff_date = datetime.now() - timedelta(days=days)
        recent_reviews = []
        
        for file_path in review_files:
            try:
                with open(file_path, 'r') as f:
                    review_data = json.load(f)
                
                review_date = datetime.fromisoformat(review_data['review_date'])
                if review_date >= cutoff_date:
                    recent_reviews.append(review_data)
            except Exception as e:
                print(f"Error reading review file {file_path}: {e}")
        
        return sorted(recent_reviews, key=lambda x: x['review_date'], reverse=True)