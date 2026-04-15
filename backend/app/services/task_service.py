import uuid

from sqlalchemy.orm import Session
from sqlalchemy import func
from app.db import models
from app.db.models import TaskStatus
from app.utils.errors import not_found, forbidden

def create_task(db: Session, project, data, user_id):
    task = models.Task(
        title=data.title,
        description=data.description,
        project_id=project.id,
        assignee_id=data.assignee_id,
        status=TaskStatus.todo,
        created_by=uuid.UUID(user_id)
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

def get_tasks(db: Session, project, status=None, assignee=None, page=1, limit=10):
    query = db.query(models.Task).filter(models.Task.project_id == project.id)

    if status:
        query = query.filter(models.Task.status == status)

    if assignee:
        query = query.filter(models.Task.assignee_id == assignee)

    return query.offset((page-1)*limit).limit(limit).all()

def get_task(db: Session, task_id: str):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        not_found()
    return task

def check_task_permission(task, project, user_id):
    # Allow if project owner
    if str(project.owner_id) == user_id:
        return

    # Allow if task creator
    if str(task.created_by) == user_id:
        return

    forbidden()

def update_task(db: Session, task, data):
    for field, value in data.dict(exclude_unset=True).items():
        setattr(task, field, value)

    db.commit()
    db.refresh(task)
    return task

def delete_task(db: Session, task):
    db.delete(task)
    db.commit()

def get_project_stats(db: Session, project):
    status_counts = db.query(
        models.Task.status,
        func.count(models.Task.id)
    ).filter(models.Task.project_id == project.id).group_by(models.Task.status).all()

    assignee_counts = db.query(
        models.Task.assignee_id,
        func.count(models.Task.id)
    ).filter(models.Task.project_id == project.id).group_by(models.Task.assignee_id).all()

    return {
        "by_status": dict(status_counts),
        "by_assignee": {str(k): v for k, v in assignee_counts}
    }