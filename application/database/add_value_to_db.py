import random
from string import ascii_letters

from models import Student, Course, Group
from db import engine

from sqlalchemy.orm import sessionmaker


Session = sessionmaker(engine)


def random_string(length):
    return "".join(random.choices(population=ascii_letters, k=length))


group = [f"{random_string(2).upper()}-{random.randint(10, 100)}" for _ in range(10)]

result_group = [Group(id=index, name=element) for index, element in enumerate(group, 1)]

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

result_courses = [Course(name=elements, description=random_string(length=20)) for elements in courses]

students = [Student(
    first_name=random.choice(students_first_name),
    last_name=random.choice(students_last_name),
    group_id=random.choice(range(1, 11)),
) for _ in range(200)]


with engine.connect() as connection:
    with Session(bind=connection) as session:
        session.add_all(result_courses)
        session.commit()
        session.add_all(result_group)
        session.commit()
        session.add_all(students)
        session.commit()

        all_student = [el.course.extend(random.sample(result_courses, random.randint(1, 3))) for el in
                               session.query(Student).filter().all()]
        session.commit()


