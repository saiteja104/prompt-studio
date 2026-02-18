from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.project import Project
from app.models.project_member import ProjectMember
from app.models.user import User
from app.schemas.project import ProjectCreate, ProjectUpdate, ProjectResponse
from app.services.auth_service import get_current_user

router = APIRouter(prefix="/projects", tags=["Projects"])

@router.get("", response_model=List[ProjectResponse])
def list_projects(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Return projects where user is a member
    memberships = db.query(ProjectMember).filter(
        ProjectMember.user_id == current_user.id
    ).all()
    project_ids = [m.project_id for m in memberships]
    return db.query(Project).filter(Project.id.in_(project_ids)).all()

@router.post("", response_model=ProjectResponse)
def create_project(
    payload: ProjectCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Create project
    project = Project(
        created_by=current_user.id,
        name=payload.name,
        description=payload.description
    )
    db.add(project)
    db.flush()  # get project.id before commit

    # Auto add creator as owner in project_members
    member = ProjectMember(
        project_id=project.id,
        user_id=current_user.id,
        role="owner"
    )
    db.add(member)
    db.commit()
    db.refresh(project)
    return project

@router.get("/{project_id}", response_model=ProjectResponse)
def get_project(
    project_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    member = db.query(ProjectMember).filter(
        ProjectMember.project_id == project_id,
        ProjectMember.user_id == current_user.id
    ).first()
    if not member:
        raise HTTPException(status_code=404, detail="Project not found")

    return db.query(Project).filter(Project.id == project_id).first()

@router.put("/{project_id}", response_model=ProjectResponse)
def update_project(
    project_id: str,
    payload: ProjectUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    member = db.query(ProjectMember).filter(
        ProjectMember.project_id == project_id,
        ProjectMember.user_id == current_user.id,
        ProjectMember.role.in_(["owner", "editor"])
    ).first()
    if not member:
        raise HTTPException(status_code=403, detail="Not authorized")

    project = db.query(Project).filter(Project.id == project_id).first()
    if payload.name is not None:
        project.name = payload.name
    if payload.description is not None:
        project.description = payload.description

    db.commit()
    db.refresh(project)
    return project

@router.delete("/{project_id}")
def delete_project(
    project_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    member = db.query(ProjectMember).filter(
        ProjectMember.project_id == project_id,
        ProjectMember.user_id == current_user.id,
        ProjectMember.role == "owner"
    ).first()
    if not member:
        raise HTTPException(status_code=403, detail="Only owner can delete project")

    project = db.query(Project).filter(Project.id == project_id).first()
    db.delete(project)
    db.commit()
    return {"message": "Project deleted"}

@router.post("/{project_id}/members")
def add_member(
    project_id: str,
    user_email: str,
    role: str = "editor",
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Only owner can add members
    owner = db.query(ProjectMember).filter(
        ProjectMember.project_id == project_id,
        ProjectMember.user_id == current_user.id,
        ProjectMember.role == "owner"
    ).first()
    if not owner:
        raise HTTPException(status_code=403, detail="Only owner can add members")

    # Find user by email
    user = db.query(User).filter(User.email == user_email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Check already a member
    existing = db.query(ProjectMember).filter(
        ProjectMember.project_id == project_id,
        ProjectMember.user_id == user.id
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="User already a member")

    member = ProjectMember(
        project_id=project_id,
        user_id=user.id,
        role=role
    )
    db.add(member)
    db.commit()
    return {"message": f"{user.name} added as {role}"}