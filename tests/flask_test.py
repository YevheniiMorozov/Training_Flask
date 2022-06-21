import pytest

from flask import url_for

from sqlalchemy import create_engine

from application.database.models import Student, Course, Group
from application import POSTGRES_TEST, Base


@pytest.fixture(scope="session")
def app():
    from application.app import app, SessionLocal

    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = POSTGRES_TEST
    engine_test = create_engine(app.config["SQLALCHEMY_DATABASE_URI"])

    Base.metadata.bind = engine_test
    SessionLocal.configure(bind=engine_test)
    session = SessionLocal()

    Base.metadata.drop_all(engine_test)
    Base.metadata.create_all(engine_test)
    with app.app_context():
        group = [Group(id=100, name="FOOBAR"), Group(id=200, name="foobar")]
        students = [
            Student(first_name="FOO", last_name="BAR", group_id=100),
            Student(first_name="oof", last_name="rab", group_id=100),
            Student(first_name="foo", last_name="bar", group_id=200),
            Student(first_name="ofo", last_name="arb", group_id=200)]
        courses = [Course(id=15, name="Bio", description="bio"),
                   Course(id=25, name="Python", description="snake"),
                   Course(id=35, name="C", description="father"),
                   Course(id=36, name="C++", description="brother"),]

        session.add_all(group)
        session.commit()
        session.add_all(students)
        session.commit()
        session.add_all(courses)
        session.commit()
        [el.course.extend(courses) for el in session.query(Student).filter(Student.id < 3).all()]
        session.commit()

    yield app


@pytest.fixture
def client(app):
    yield app.test_client()


@pytest.fixture
def ctx(app):
    with app.test_request_context() as context:
        yield context


def test_api_groups(client, ctx):
    url = url_for("allgroups", format="json")
    resp = client.get(url)
    data = resp.json
    assert "2" in data
    assert "foobar" in data["2"]["name"]
    assert "1" in data
    assert "FOOBAR" in data["1"]["name"]


def test_api_courses(client, ctx):
    url = url_for("allcourses", format="json")
    resp = client.get(url)
    data = resp.json
    assert "15" in data
    assert "Bio" in data["15"]["name"]
    assert "25" in data
    assert "Python" in data["25"]["name"]
    assert "35" in data
    assert "C" in data["35"]["name"]
    assert "C++" in data["36"]["name"]


def test_api_students(client, ctx):
    url = url_for("allstudents", format="json")
    resp = client.get(url)
    data = resp.json
    assert "1" in data
    assert "ofo" in data["1"]["first name"]
    assert "arb" in data["1"]["last name"]
    assert "2" in data
    assert "foo" in data["2"]["first name"]
    assert "bar" in data["2"]["last name"]

    url = url_for("allstudents")
    response = client.post(url, json={
        "firstname": "Josephina",
        "lastname": "Gachina",
        "group_id": "200",
    })
    assert response.status_code == 200
    assert response.json == {"message": "Successfully added"}

    url = url_for("allstudents", delete_by_id="4")
    resp = client.delete(url)
    assert resp.json == {"message": "Successfully deleted"}


def test_api_student_course(client, ctx):
    url = url_for("studentcourse", format="json", student_id="1")
    resp = client.get(url)
    data = resp.json
    assert "FOO" in data["Firstname"]
    assert "BAR" in data["Lastname"]
    assert "Python" in data["Courses"]["1"]["name"]
    assert "C" in data["Courses"]["2"]["name"]

    url = url_for("studentcourse", student_id="1", course_id="15")
    response = client.post(url)
    assert response.status_code == 200
    assert response.json == {"message": "Successfully added"}
    response = client.post(url)
    assert response.status_code == 200
    assert response.json == {"message": "Student is already on it"}
    url = url_for("studentcourse", student_id="1", course_id="16")
    response = client.post(url)
    assert response.status_code == 200
    assert response.json == {"message": "Course does not exist"}

    url = url_for("studentcourse", student_id="1", course_id="15")
    resp = client.delete(url)
    assert resp.json == {"message": "Successfully deleted"}
