from datetime import datetime, timedelta
from workflow_engine import WorkflowEngine

def main():
    engine = WorkflowEngine()
    
    print("=== MVP End-to-End Workflow Demo ===\n")
    
    # Demo 1: Complete end-to-end flow
    print("1. Running complete end-to-end flow...")
    result = engine.end_to_end_flow(
        title="User Authentication",
        description="Implement login and registration functionality",
        priority="high",
        version="v1.0.0",
        assignee="john.doe",
        estimated_hours=40
    )
    
    print(f"✓ Feature created: {result['feature'].id}")
    print(f"✓ Release prepared: {result['release'].id} ({result['release'].version})")
    print(f"✓ Status: {result['status']}\n")
    
    # Demo 2: Individual feature intake
    print("2. Adding individual features...")
    feature1 = engine.intake_service.submit_feature_request(
        "Password Reset", "Allow users to reset forgotten passwords", "medium"
    )
    feature2 = engine.intake_service.submit_feature_request(
        "Email Notifications", "Send email alerts for important events", "low"
    )
    
    print(f"✓ Added feature: {feature1.id}")
    print(f"✓ Added feature: {feature2.id}\n")
    
    # Demo 3: Pipeline status
    print("3. Current pipeline status:")
    status = engine.get_pipeline_status()
    for status_name, count in status["features_by_status"].items():
        print(f"   {status_name}: {count}")
    print(f"   Total features: {status['total_features']}")
    print(f"   Total releases: {status['total_releases']}\n")
    
    print("Demo completed successfully!")

if __name__ == "__main__":
    main()