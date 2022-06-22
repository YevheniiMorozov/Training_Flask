import random
from string import ascii_letters

from models import StudentCourseAssoc, Student, Course, Group
from application import Base

from application.init_db import Session, engine


def random_string(length):
    return "".join(random.choices(population=ascii_letters, k=length))


group = [f"{random_string(2).upper()}-{random.randint(10, 100)}" for _ in range(10)]

students_first_name = [
    "Adam", "Nathan", "Jack", "Alexander",
    "Jose", "Keith", "Harold", "Carl",
    "Arthur", "Lawrence", "Billy", "Alan",
    "Louis", "Grace", "Kathryn", "Gloria",
    "Judith", "Victoria", "Debra", "Nicole"
]
students_last_name = [
    "Smith", "Johnson", "Brown", "Miller",
    "Wilson", "Taylor", "Moore", "Martin",
    "Lee", "Thompson", "Clark", "Lewis",
    "Allen", "Wright", "Torres", "Hill",
    "Green", "Baker", "Carter", "Parker"
]

courses = ["Math", "Biology", "Chemistry", "Physics", "English", "Economy",
           "You know the rules", "And so do I", "Never gonna", "Give you up"]

students = [Student(
    first_name=random.choice(students_first_name),
    last_name=random.choice(students_last_name),
    group_id=random.choice(range(1, 11)),
) for _ in range(200)]

result_group = [Group(name=element) for element in group]
result_courses = [Course(name=elements, description=random_string(length=20)) for elements in courses]


if __name__ == '__main__':

    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    with engine.connect() as connection:
        with Session(bind=connection) as session:
            session.add_all(result_group)
            session.commit()
            session.add_all(result_courses)
            session.commit()
            session.add_all(students)
            session.commit()
            st_crs = []
            for el in students:
                for crs in random.sample(result_courses, random.randint(1, 3)):
                    st_crs.append(StudentCourseAssoc(student_id=el.id, course_id=crs.id))
            session.add_all(st_crs)
            session.commit()

