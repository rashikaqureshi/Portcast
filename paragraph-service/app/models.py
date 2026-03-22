from sqlalchemy import Column, Integer, Text
from .database import Base

class Paragraph(Base):
    __tablename__ = "paragraphs"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)