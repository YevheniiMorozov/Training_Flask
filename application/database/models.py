from application import Base
from application.init_db import engine
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship


Base.metadata.clear()


class Group(Base):
    __table_args__ = {'extend_existing': True}
    __tablename__ = "group"

    id = Column(Integer, primary_key=True)
    name = Column(String(20), nullable=False)


class Student(Base):
    __table_args__ = {'extend_existing': True}
    __tablename__ = "student"

    id = Column(Integer, primary_key=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    group_id = Column(ForeignKey(Group.id))
    group = relationship(Group)


class Course(Base):
    __table_args__ = {'extend_existing': True}
    __tablename__ = "course"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(String(250), nullable=False)


class StudentCourseAssoc(Base):
    __table_args__ = {'extend_existing': True}
    __tablename__ = "student_course_assoc"

    student_id = Column(ForeignKey(Student.id), primary_key=True)
    student = relationship(Student)
    course_id = Column(ForeignKey(Course.id), primary_key=True)
    course = relationship(Course)


if __name__ == '__main__':
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
