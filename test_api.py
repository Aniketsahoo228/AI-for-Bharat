"""
Quick Test Script - Verify API Works
Run this to test all endpoints
"""

from main_working import app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_health():
    """Test health endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    print("✓ Health check passed")

def test_register_and_login():
    """Test registration and login"""
    # Register
    response = client.post("/api/auth/register", json={
        "email": "test@example.com",
        "username": "testuser",
        "password": "password123",
        "full_name": "Test User"
    })
    assert response.status_code == 200
    data = response.json()
    token = data["access_token"]
    user_id = data["user_id"]
    print(f"✓ Registration passed - User ID: {user_id}")
    
    # Login
    response = client.post("/api/auth/login", json={
        "email": "test@example.com",
        "password": "password123"
    })
    assert response.status_code == 200
    print("✓ Login passed")
    
    # Get current user
    response = client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    print(f"✓ Get current user passed")
    
    return token, user_id

def test_pdf_workflow(token, user_id):
    """Test PDF and workflow generation"""
    # List PDFs (should be empty)
    response = client.get("/api/pdfs", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    print(f"✓ PDF listing passed - Count: {len(response.json())}")
    
    # Capture text
    response = client.post("/api/capture/text", 
        headers={"Authorization": f"Bearer {token}"},
        json={
            "pdf_id": 1,
            "text": "Machine learning is a subset of artificial intelligence that enables systems to learn and improve from experience.",
            "page_number": 1
        }
    )
    assert response.status_code == 200
    capture_id = response.json()["id"]
    print(f"✓ Text capture passed - Capture ID: {capture_id}")
    
    # Generate workflow
    response = client.post("/api/workflow/generate",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "pdf_id": 1,
            "capture_ids": [capture_id]
        }
    )
    assert response.status_code == 200
    workflow = response.json()
    workflow_id = workflow["id"]
    print(f"✓ Workflow generation passed - Workflow ID: {workflow_id}")
    
    # Get workflows
    response = client.get("/api/workflows", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    workflows = response.json()
    print(f"✓ Workflow listing passed - Count: {len(workflows)}")
    
    return workflow_id

def test_summaries(token, workflow_id):
    """Test summary generation"""
    response = client.get(f"/api/workflow/{workflow_id}", headers={"Authorization": f"Bearer {token}"})
    workflow = response.json()
    
    if workflow.get("steps"):
        step = workflow["steps"][0]
        response = client.post("/api/summaries/generate",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "workflow_id": workflow_id,
                "step_id": step.get("id", "step_0"),
                "language": "English"
            }
        )
        assert response.status_code == 200
        summary = response.json()
        print(f"✓ Summary generation passed - Summary ID: {summary['id']}")

if __name__ == "__main__":
    try:
        print("Running API Tests...")
        print("-" * 50)
        
        test_health()
        token, user_id = test_register_and_login()
        workflow_id = test_pdf_workflow(token, user_id)
        test_summaries(token, workflow_id)
        
        print("-" * 50)
        print("✓ All tests passed!")
        print()
        print("Backend is fully functional!")
        print()
        print("To start the server, run:")
        print("  python main_working.py")
        print()
        print("Server will be available at:")
        print("  http://localhost:8000")
        print("  Docs: http://localhost:8000/docs")
        
    except Exception as e:
        print(f"✗ Test failed: {e}")
        import traceback
        traceback.print_exc()
