from sqlalchemy import Column, String, Text, Integer, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from app.database import Base
import uuid
from datetime import datetime

class RunResult(Base):
    __tablename__ = "run_results"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    run_id = Column(UUID(as_uuid=True), ForeignKey("runs.id", ondelete="CASCADE"), nullable=False)
    model_id = Column(UUID(as_uuid=True), ForeignKey("llm_models.id", ondelete="SET NULL"), nullable=True)
    response = Column(Text)
    input_tokens = Column(Integer)
    output_tokens = Column(Integer)
    latency_ms = Column(Integer)
    status = Column(String(50))
    error = Column(Text)
    model_params = Column(JSONB, default={})
    created_at = Column(DateTime, default=datetime.utcnow)

    run = relationship("Run", back_populates="results")
    model = relationship("LLMModel", back_populates="run_results")