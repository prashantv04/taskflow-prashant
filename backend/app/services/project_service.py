from sqlalchemy.orm import Session
# from sqlalchemy import or_
from app.db import models
from app.utils.errors import not_found, forbidden

def create_project(db: Session, user_id: str, data):
    project = models.Project(
        name=data.name,
        description=data.description,
        owner_id=user_id
    )
    db.add(project)
    db.commit()
    db.refresh(project)
    return project

def get_projects(db: Session, user_id: str, page: int = 1, limit: int = 10):
    offset = (page - 1) * limit

    return db.query(models.Project).filter(
        models.Project.owner_id == user_id
    ).offset(offset).limit(limit).all()

def get_project(db: Session, project_id: str, user_id: str):
    project = db.query(models.Project).filter(
        models.Project.id == project_id
    ).first()

    if not project:
        not_found()

    if str(project.owner_id) != user_id:
        forbidden()

    return project

def update_project(db: Session, project, data):
    if data.name:
        project.name = data.name
    if data.description:
        project.description = data.description

    db.commit()
    db.refresh(project)
    return project

def delete_project(db: Session, project):
    db.delete(project)
    db.commit()