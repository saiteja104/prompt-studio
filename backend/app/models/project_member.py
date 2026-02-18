from sqlalchemy import Column, String, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.database import Base
import uuid
from datetime import datetime

class ProjectMember(Base):
    __tablename__ = "project_members"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    role = Column(String(50), default="editor")  # owner, editor, viewer
    joined_at = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (UniqueConstraint("project_id", "user_id", name="unique_project_member"),)

    project = relationship("Project", back_populates="members")
    user = relationship("User", back_populates="project_memberships")