import unittest
from fastapi.testclient import TestClient
from unittest.mock import patch
from app.api.main import app
from app.api.tasks import tasks
from app.api.users import users
from app.repository.mock_task_repository import TaskRepoImplementation as MockTaskRepo
from app.repository.mock_user_repository import UsersRepoImplementation as MockUserRepo


app.user_middleware.clear()
@app.middleware("http")
async def mock_auth_middleware(request, call_next):
    request.state.user = "test_user"
    response = await call_next(request)
    return response

app.middleware_stack = app.build_middleware_stack()


class TestMain(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        tasks.task_use_case.repo = MockTaskRepo()
        tasks.user_use_case.repository = MockUserRepo()
        users.use_case.repository = MockUserRepo()
        cls.client = TestClient(app)

    @classmethod
    def tearDownClass(cls):
        patch.stopall()


    def test_create_task(self):
        params = {
            "title": "string",
            "description": "string",
            "due_date": "2025-03-10T13:52:29.612Z",
            "assigned_to": "testuser"
        }
        response = self.client.post("/tasks/create/", json=params)
        assert response.status_code == 201

    def test_get_task_with_valid_code(self):
        response = self.client.get("/tasks/task/test_code")
        assert response.status_code == 200

    def test_get_task_invalid_code(self):
        response = self.client.get("/tasks/task/invalid_code")
        assert response.status_code == 404

    def test_update_task(self):
        params = {
          "title": "string",
          "description": "string",
          "due_date": "2025-03-10T14:44:24.799Z",
          "assigned_to": "string",
          "status": "new"
        }
        response = self.client.put("/tasks/test_code", json=params)
        assert response.status_code == 200

    def test_invalid_code_when_update_task(self):
        params = {
            "title": "string",
            "description": "string",
            "due_date": "2025-03-10T14:44:24.799Z",
            "assigned_to": "string",
            "status": "new"
        }
        response = self.client.put("/tasks/test_invalid_code", json=params)
        assert response.status_code == 404

    def test_create_user(self):
        params = {
          "username": "valid_user",
          "email": "valid_user_@valid.com",
          "password": "some_passwrod"
        }
        response = self.client.post("/users", json=params)
        assert response.status_code == 200

    def test_delete_task(self):
        response = self.client.delete("/tasks/test_code")
        assert response.status_code == 204

    def test_invalid_code_when_delete(self):
        response = self.client.delete("/tasks/not_valid")
        assert response.status_code == 404

    def test_task_filter(self):
        params = {"date_from": "2025-01-01", "date_to": "2025-12-31", "status": "new", "page": 1, "size": 10}
        response = self.client.get("/tasks/filter", params=params)
        assert response.status_code == 200
        assert len(response.json()) > 0


    def test_update_status(self):
        response = self.client.put("/tasks/complete/test_code")
        assert response.status_code == 201
