from sqlalchemy import func
from sqlalchemy.orm import Session

from .models import Student, Course, Group


def get_all_(db: Session, course_id=None):
    if course_id:
        return db.query(Student).join(Course.student).order_by(Student.last_name).filter(Course.id == course_id).all()
    return db.query(Student).order_by(Student.last_name).filter().all()


def get_courses(db: Session):
    return db.query(Course).order_by(Course.id).all()


def get_groups(db: Session, all=None):
    group_data = db.query(func.count(Student.group_id), Student.group_id, Group.name
                          ).group_by(Student.group_id, Group.id).filter(Student.group_id == Group.id)
    group_data = sorted(group_data, key=lambda x: x[0])
    min_group = group_data[0][0]
    if all:
        return group_data
    return filter(lambda x: x[0] == min_group, group_data)


def get_students_course(db: Session, student_id: int):
    return db.query(Student).filter(Student.id == student_id).one()


def remove_from_course(db: Session, course_id, student_id):
    student = db.query(Student).filter(Student.id == student_id).first()
    course = db.query(Course).filter(Course.id == course_id).first()
    student.course.remove(course)
    return db.commit()


def add_new_student(db: Session, first, last, group):
    student = Student(first_name=first,
                      last_name=last,
                      group_id=int(group))
    db.add(student)

    return db.commit()


def add_student_to_course(db: Session, user_id, course_id):
    student = db.query(Student).filter(
        Student.id == user_id).first()
    course = db.query(Course).filter(Course.id == course_id).first()
    student.course.append(course)
    return db.commit()


def delete_student(db: Session, student_id: int):
    db.query(Student).filter(Student.id == student_id).delete()
    return db.commit()

