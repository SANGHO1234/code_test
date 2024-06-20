from sqlalchemy import Column, Integer, String, Text, DateTime
from database import Base

class SubmissionModel(Base):
    __tablename__ = "submission"

    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    status = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)

    def __str__(self):
        return str(self.id)