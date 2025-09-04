from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
import uvicorn

from .models import WorkflowRequest, WorkflowResult
from .crew_runner import CrewAIRunner
from .config import settings

app = FastAPI(title="CrewAI Workflow Runner", version="1.0.0")
runner = CrewAIRunner()


@app.get("/health")
async def health_check():
    """Health check endpoint for container monitoring."""
    return {"status": "healthy", "environment": settings.environment}


@app.post("/workflows", response_model=WorkflowResult)
async def execute_workflow(request: WorkflowRequest, background_tasks: BackgroundTasks):
    """Execute a CrewAI workflow."""
    try:
        # Validate request
        if not request.agents:
            raise HTTPException(status_code=400, detail="At least one agent is required")
        
        if not request.tasks:
            raise HTTPException(status_code=400, detail="At least one task is required")
        
        # Start workflow execution in background
        background_tasks.add_task(runner.execute_workflow, request)
        
        # Return initial status
        return WorkflowResult(
            workflow_id=request.workflow_id,
            status="pending",
            started_at=datetime.utcnow()
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/workflows/{workflow_id}", response_model=WorkflowResult)
async def get_workflow_status(workflow_id: str):
    """Get the status of a workflow."""
    try:
        return runner.get_workflow_status(workflow_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.delete("/workflows/{workflow_id}")
async def cancel_workflow(workflow_id: str):
    """Cancel a running workflow."""
    success = runner.cancel_workflow(workflow_id)
    if not success:
        raise HTTPException(status_code=404, detail="Workflow not found or not running")
    
    return {"message": "Workflow cancelled successfully"}


@app.get("/workflows")
async def list_workflows():
    """List all workflows and their statuses."""
    return {"workflows": list(runner.active_workflows.values())}