from sqlalchemy import Column, Integer, Text, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
import json
from config import DATABASE_URL

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
Base = declarative_base()


class Job(Base):
    __tablename__ = "jobs"
    id = Column(Text, primary_key=True)
    title = Column(Text, nullable=False)
    company = Column(Text, nullable=False)
    industry = Column(Text, nullable=False)
    description = Column(Text, nullable=False)
    required_skills = Column(Text, nullable=False)
    required_experience_years = Column(Integer)
    required_education = Column(Text)
    created_at = Column(Text)

    def skills_list(self) -> list:
        return json.loads(self.required_skills)


def get_db():
    Session = sessionmaker(bind=engine)
    return Session()
