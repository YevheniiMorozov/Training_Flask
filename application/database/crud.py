import random
from string import ascii_letters

from models import Student, Course, Group
from .database import engine

from sqlalchemy.orm import sessionmaker


Session = sessionmaker(engine)


def random_string(length):
    return "".join(random.choices(population=ascii_letters, k=length))


result_group = [Group(name=f"{random_string(2).upper()}-{random.randint(10, 100)}") for _ in range(10)]

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

result_students = [Student(
    first_name=random.choice(students_first_name),
    last_name=random.choice(students_last_name),
    group_id=random.choice(result_group),
    course=random.choices(result_courses, k=random.choice(range(1, 4)))
)]


with engine.connect() as connection:
    with Session(bind=connection) as session:
        session.add_all(result_courses)
        session.commit()
        session.add_all(result_group)
        session.commit()
        session.add_all(result_students)
        session.commit()