from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from app.database import Base
import uuid
from datetime import datetime

class ActivityLog(Base):
    __tablename__ = "activity_log"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    prompt_id = Column(UUID(as_uuid=True), ForeignKey("prompts.id", ondelete="CASCADE"), nullable=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    action = Column(String(100), nullable=False)
    extra_data = Column(JSONB, default={})
    created_at = Column(DateTime, default=datetime.utcnow)

    project = relationship("Project", back_populates="activity_logs")
    user = relationship("User", back_populates="activity_logs")
    prompt = relationship("Prompt", back_populates="activity_logs")