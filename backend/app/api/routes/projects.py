from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from app.api.deps import get_current_user
from app.db.session import SessionLocal
from app.schemas.project import ProjectCreate, ProjectUpdate
from app.services import project_service, task_service

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/")
def list_projects(
    page: int = Query(1),
    limit: int = Query(10),
    user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return project_service.get_projects(db, user["user_id"], page, limit)

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_project(data: ProjectCreate, user=Depends(get_current_user), db: Session = Depends(get_db)):
    return project_service.create_project(db, user["user_id"], data)

@router.get("/{project_id}")
def get_project(project_id: str, user=Depends(get_current_user), db: Session = Depends(get_db)):
    return project_service.get_project(db, project_id, user["user_id"])

@router.patch("/{project_id}")
def update_project(project_id: str, data: ProjectUpdate, user=Depends(get_current_user), db: Session = Depends(get_db)):
    project = project_service.get_project(db, project_id, user["user_id"])
    return project_service.update_project(db, project, data)

@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(project_id: str, user=Depends(get_current_user), db: Session = Depends(get_db)):
    project = project_service.get_project(db, project_id, user["user_id"])
    project_service.delete_project(db, project)

@router.get("/{project_id}/stats")
def project_stats(project_id: str, user=Depends(get_current_user), db: Session = Depends(get_db)):
    project = project_service.get_project(db, project_id, user["user_id"])
    return task_service.get_project_stats(db, project)