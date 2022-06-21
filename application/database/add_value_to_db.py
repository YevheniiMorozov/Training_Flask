import random
from string import ascii_letters

from models import StudentCourseAssoc, Student, Course, Group
from application import engine, Base

from application.app import SessionLocal


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

result_group = [Group(id=index, name=element) for index, element in enumerate(group, 1)]
result_courses = [Course(name=elements, description=random_string(length=20)) for elements in courses]

Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

with engine.connect() as connection:
    with SessionLocal(bind=connection) as session:
        session.add_all(result_courses)
        session.commit()
        session.add_all(students)
        session.commit()
        session.add_all(result_group)
        session.commit()
        # s = Student()
        # st_course = StudentCourseAssoc()
        # st_course.course = Course()
        # s.course.append(st_course)
        # all_students = [el.course.extend(random.sample(st_course.course, random.randint(1, 3)))
        #                 for el in session.query(Student).filter().all()]
        # all_student = [el.course.extend(random.sample(result_courses, random.randint(1, 3))) for el in
        #                        session.query(Student).filter().all()]
        session.commit()


