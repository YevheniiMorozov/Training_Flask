from sqlalchemy import func
from sqlalchemy.orm import Session

from .models import Student, Course, Group, StudentCourseAssoc


def get_all_(db: Session, course_id=None):
    query = db.query(Student).order_by(Student.last_name)
    if course_id:
        query = db.query(Student).join(Course.student).order_by(Student.last_name).filter(Course.id == course_id).all()
    return query


def get_courses(db: Session):
    return db.query(Course).order_by(Course.id).all()


def get_groups(db: Session, all=False):
    group_data = db.query(Group.name, Student.group_id, func.count(Student.group_id)).join(Student).group_by(
        Group.id, Student.group_id).all()
    group_data = sorted(group_data, key=lambda x: x[2])
    min_group = group_data[0][2]
    if all:
        return group_data
    return filter(lambda x: x[0] == min_group, group_data)


def get_student_course(db: Session, student_id: int):
    if student_id:
        return db.query(StudentCourseAssoc).filter(StudentCourseAssoc.student_id == student_id).all()
    return {"message": "Please, input student id"}


def remove_from_course(db: Session, course_id, student_id):
    if student_id and course_id:
        db.query(StudentCourseAssoc).filter(
            StudentCourseAssoc.student_id == student_id).filter(
            StudentCourseAssoc.course_id == course_id).delete()
        db.commit()
        return {"message": "Successfully deleted"}
    return {"message": "Incorrect input student id or course id"}


def add_new_student(db: Session, first, last, group):
    student = Student(first_name=first,
                      last_name=last,
                      group_id=int(group))
    db.add(student)

    return db.commit()


def add_student_to_course(db: Session, user_id: int, course_id: int):

    student = db.query(Student).filter(Student.id == user_id).first()
    course = db.query(Course).filter(Course.id == course_id).first()
    if student and course:
        db.add(StudentCourseAssoc(student_id=user_id, course_id=course_id))
        db.commit()
        return {"message": "Successfully added"}
    return {"message": "Incorrect data input"}


def delete_student(db: Session, student_id: int):
    if student_id:
        db.query(Student).filter(Student.id == student_id).delete()
        db.commit()
        return {"message": "Successfully deleted"}
    return {"message": "Incorrect input student id"}


def add_new_course(db: Session, course_name: str, description: str):
    course = Course(name=course_name, description=description)
    db.add(course)
    db.commit()
    return {"message": "Successfully added"}


def get_course(db: Session, course_id: int):
    return db.query(Course).filter(Course.id == course_id).first()


def delete_course(db: Session, course_id: int):
    if course_id:
        db.query(Course).filter(Course.id == course_id).delete()
        db.commit()
        return {"message": "Successfully deleted"}
    return {"message": "Incorrect input course id"}


def add_new_group(db: Session, group_name: str):
    db.add(Group(name=group_name))
    db.commit()
    return {"message": "Successfully added"}


def delete_group(db: Session, group_id: int):
    if group_id:
        db.query(Group).filter(Group.id == group_id).delete()
        db.commit()
        return {"message": "Successfully deleted"}
    return {"message": "Incorrect input group id"}


