# from application import Base, engine
#
# from sqlalchemy import Column, Integer, String, sql, ForeignKey, Table
# from sqlalchemy.orm import relationship
#
# from application import Base, engine
#
#
# association_table = Table("association", Base.metadata,
#                           Column("student_id", ForeignKey("student.id"), primary_key=True),
#                           Column("course_id", ForeignKey("course.id"), primary_key=True))
#
#
# class Group(Base):
#     __table_args__ = {'extend_existing': True}
#     __tablename__ = "group"
#
#     id = Column(Integer, primary_key=True)
#     name = Column(String(20), nullable=False)
#     student = relationship("Student", backref="group")
#
#
# class Student(Base):
#     __table_args__ = {'extend_existing': True}
#     __tablename__ = "student"
#
#     id = Column(Integer, primary_key=True)
#     first_name = Column(String(50), nullable=False)
#     last_name = Column(String(50), nullable=False)
#     group_id = Column(Integer, ForeignKey("group.id"))
#     course = relationship("Course", secondary=association_table, back_populates="student")
#
#
# class Course(Base):
#     __table_args__ = {'extend_existing': True}
#     __tablename__ = "course"
#
#     id = Column(Integer, primary_key=True)
#     name = Column(String(100), nullable=False)
#     description = Column(String(250), nullable=False)
#     student = relationship("Student", secondary=association_table, back_populates="course")
#
#
# if __name__ == '__main__':
#     Base.metadata.drop_all(engine)
#     Base.metadata.create_all(engine)
#


from application import Base, engine

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship


Base.metadata.clear()


class Group(Base):
    __table_args__ = {'extend_existing': True}
    __tablename__ = "group"

    id = Column(Integer, primary_key=True)
    name = Column(String(20), nullable=False)
    student = relationship("Student")


class StudentCourseAssoc(Base):
    __table_args__ = {'extend_existing': True}
    __tablename__ = "student_course_assoc"

    student_id = Column(Integer, ForeignKey("student.id"), primary_key=True)
    course_id = Column(Integer, ForeignKey("course.id"), primary_key=True)


class Student(Base):
    __table_args__ = {'extend_existing': True}
    __tablename__ = "student"

    id = Column(Integer, primary_key=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    group_id = Column(Integer, ForeignKey("group.id"))
    course = relationship("StudentCourseAssoc")


class Course(Base):
    __table_args__ = {'extend_existing': True}
    __tablename__ = "course"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(String(250), nullable=False)
    student = relationship("StudentCourseAssoc")


if __name__ == '__main__':
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
