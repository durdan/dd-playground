import os
from dotenv import load_dotenv
from service import CodeReviewService
from models import CodeReviewRequest, ReviewType

def main():
    load_dotenv()
    
    # Ensure OpenAI API key is set
    if not os.getenv("OPENAI_API_KEY"):
        raise ValueError("OPENAI_API_KEY environment variable is required")
    
    service = CodeReviewService()
    
    # Example usage
    sample_code = """
def login(username, password):
    query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
    result = db.execute(query)
    if result:
        return True
    return False

def process_data(data):
    results = []
    for i in range(len(data)):
        for j in range(len(data)):
            if data[i] == data[j] and i != j:
                results.append(data[i])
    return results
    """
    
    request = CodeReviewRequest(
        file_path="auth.py",
        code_content=sample_code,
        review_types=[ReviewType.SECURITY, ReviewType.QUALITY, ReviewType.PERFORMANCE]
    )
    
    try:
        result = service.review_code(request)
        print(f"Review Results for {result.file_path}")
        print(f"Overall Score: {result.overall_score}/10")
        print(f"Summary: {result.summary}")
        print("\nIssues Found:")
        
        for issue in result.issues:
            print(f"- [{issue.type.value.upper()}] {issue.severity.upper()}: {issue.description}")
            if issue.line_number:
                print(f"  Line: {issue.line_number}")
            print(f"  Suggestion: {issue.suggestion}")
            print()
            
    except Exception as e:
        print(f"Error during code review: {e}")

if __name__ == "__main__":
    main()