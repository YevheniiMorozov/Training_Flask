import pytest

from flask import url_for
from application.database.models import Student, Course, Group, StudentCourseAssoc
from application import Base


@pytest.fixture(scope="session")
def app():
    from application.app import app

    app.config["TESTING"] = True
    from application.init_db import Session, engine

    Base.metadata.bind = engine
    Session.configure(bind=engine)
    session = Session()

    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    with app.app_context():
        group = [Group(name="FOOBAR"), Group(name="foobar")]
        students = [
            Student(first_name="FOO", last_name="BAR", group_id=1),
            Student(first_name="oof", last_name="rab", group_id=1),
            Student(first_name="foo", last_name="bar", group_id=2),
            Student(first_name="ofo", last_name="arb", group_id=2)]
        courses = [Course(id=15, name="Bio", description="bio"),
                   Course(id=25, name="Python", description="snake"),
                   Course(id=35, name="C", description="father"),
                   Course(id=36, name="C++", description="brother")]

        session.add_all(group)
        session.commit()
        session.add_all(students)
        session.commit()
        session.add_all(courses)
        session.commit()
        std_crs = []
        for std in students[:2]:
            for course in courses:
                std_crs.append(StudentCourseAssoc(course_id=course.id, student_id=std.id))
        session.add_all(std_crs)
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

    url = url_for("allgroups", group_name="PYTHON")
    resp = client.post(url)
    assert resp.json == {"message": "Successfully added"}

    url = url_for("allgroups", group_id=3)
    resp = client.delete(url)
    assert resp.json == {"message": "Successfully deleted"}


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

    url = url_for("allcourses")
    response = client.post(url, json={
        "name": "Mathematics",
        "description": "Science of numbers"
    })
    assert response.status_code == 200
    assert response.json == {"message": "Successfully added"}

    url = url_for("allcourses", course_id="1")
    resp = client.delete(url)
    assert resp.json == {"message": "Successfully deleted"}


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
        "group_id": "2",
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
    assert "1" in data["Student_id"]
    assert "Bio" in data["Courses"]["1"]["name"]
    assert "Python" in data["Courses"]["2"]["name"]

    url = url_for("studentcourse", student_id="3", course_id="15")
    response = client.post(url)
    assert response.status_code == 200
    assert response.json == {"message": "Successfully added"}
    url = url_for("studentcourse", student_id="1", course_id="16")
    response = client.post(url)
    assert response.status_code == 200
    assert response.json == {"message": "Incorrect data input"}

    url = url_for("studentcourse", student_id="3", course_id="15")
    resp = client.delete(url)
    assert resp.json == {"message": "Successfully deleted"}
