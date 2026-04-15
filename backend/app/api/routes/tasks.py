from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from app.api.deps import get_current_user
from app.db.session import SessionLocal
from app.schemas.task import TaskCreate, TaskUpdate
from app.services import task_service, project_service

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/projects/{project_id}/tasks")
def list_tasks(
    project_id: str,
    status: str = Query(None),
    assignee: str = Query(None),
    page: int = Query(1),
    limit: int = Query(10),
    user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    project = project_service.get_project(db, project_id, user["user_id"])
    return task_service.get_tasks(db, project, status, assignee, page, limit)


@router.post("/projects/{project_id}/tasks", status_code=status.HTTP_201_CREATED)
def create_task(project_id: str, data: TaskCreate, user=Depends(get_current_user), db: Session = Depends(get_db)):
    project = project_service.get_project(db, project_id, user["user_id"])
    return task_service.create_task(db, project, data, user["user_id"])


@router.patch("/tasks/{task_id}")
def update_task(task_id: str, data: TaskUpdate, user=Depends(get_current_user), db: Session = Depends(get_db)):
    task = task_service.get_task(db, task_id)

    # get project for auth
    project = project_service.get_project(db, str(task.project_id), user["user_id"])

    task_service.check_task_permission(task, project, user["user_id"])

    return task_service.update_task(db, task, data)


@router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: str, user=Depends(get_current_user), db: Session = Depends(get_db)):
    task = task_service.get_task(db, task_id)

    project = project_service.get_project(db, str(task.project_id), user["user_id"])

    task_service.check_task_permission(task, project, user["user_id"])

    task_service.delete_task(db, task)