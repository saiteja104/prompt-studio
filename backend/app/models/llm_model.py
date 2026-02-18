from sqlalchemy import Column, String, Boolean
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from app.database import Base
import uuid

class LLMModel(Base):
    __tablename__ = "llm_models"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    provider = Column(String(100), nullable=False)
    name = Column(String(100), nullable=False)
    display_name = Column(String(255))
    is_active = Column(Boolean, default=True)
    config = Column(JSONB, default={})

    run_results = relationship("RunResult", back_populates="model")