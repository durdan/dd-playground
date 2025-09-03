from api_docs import Endpoint, Parameter, Response, HTTPMethod

# Sample API endpoints for a user management system
def get_sample_endpoints():
    return [
        Endpoint(
            path="/users",
            method=HTTPMethod.GET,
            summary="List all users",
            description="Retrieve a paginated list of all users in the system.",
            tags=["Users"],
            query_params=[
                Parameter("page", "integer", "Page number", required=False, example=1),
                Parameter("limit", "integer", "Items per page", required=False, example=10),
                Parameter("search", "string", "Search term", required=False, example="john")
            ],
            responses=[
                Response(
                    200, 
                    "Success",
                    {
                        "users": [
                            {"id": 1, "name": "John Doe", "email": "john@example.com"},
                            {"id": 2, "name": "Jane Smith", "email": "jane@example.com"}
                        ],
                        "pagination": {"page": 1, "limit": 10, "total": 2}
                    }
                )
            ]
        ),
        
        Endpoint(
            path="/users/{user_id}",
            method=HTTPMethod.GET,
            summary="Get user by ID",
            description="Retrieve detailed information about a specific user.",
            tags=["Users"],
            path_params=[
                Parameter("user_id", "integer", "User ID", example=123)
            ],
            responses=[
                Response(
                    200,
                    "Success",
                    {"id": 123, "name": "John Doe", "email": "john@example.com", "created_at": "2023-01-01T00:00:00Z"}
                ),
                Response(404, "User not found", {"error": "User with ID 123 not found"})
            ]
        ),
        
        Endpoint(
            path="/users",
            method=HTTPMethod.POST,
            summary="Create new user",
            description="Create a new user account with the provided information.",
            tags=["Users"],
            request_body={
                "name": "John Doe",
                "email": "john@example.com",
                "password": "secure_password"
            },
            responses=[
                Response(
                    201,
                    "User created successfully",
                    {"id": 124, "name": "John Doe", "email": "john@example.com", "created_at": "2023-01-01T00:00:00Z"}
                ),
                Response(400, "Invalid input", {"error": "Email already exists"})
            ]
        ),
        
        Endpoint(
            path="/users/{user_id}",
            method=HTTPMethod.DELETE,
            summary="Delete user",
            description="Permanently delete a user account.",
            tags=["Users"],
            path_params=[
                Parameter("user_id", "integer", "User ID", example=123)
            ],
            responses=[
                Response(204, "User deleted successfully"),
                Response(404, "User not found", {"error": "User with ID 123 not found"})
            ]
        )
    ]