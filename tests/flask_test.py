import pytest

from flask import url_for

from sqlalchemy import create_engine

from application.database.models import Student, Course, Group
from application import POSTGRES_TEST, Base, SessionLocal


@pytest.fixture(scope="session")
def app():
    from application.app import app

    app.config["TESTING"] = True
    # app.config["SQLALCHEMY_DATABASE_URI"] = POSTGRES_TEST
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


def test_start_page(client, ctx):
    url = url_for("index")
    resp = client.get(url)
    url1 = url_for('all_students')
    url2 = url_for('add_new_student')
    url3 = url_for('show_all_courses')
    url4 = url_for('smallest_group')
    data = resp.data.decode("utf-8")
    assert url1 in data
    assert url2 in data
    assert url3 in data
    assert url4 in data
    assert resp.status_code == 200


def test_all_students(client, ctx):
    url = url_for('all_students')
    resp = client.get(url)
    data = resp.data.decode("utf-8")
    assert "FOO" in data
    assert "foo" in data
    assert "BAR" in data
    assert "bar" in data


def test_smallest_group(client, ctx):
    url = url_for("smallest_group")
    resp = client.get(url)
    data = resp.data.decode("utf-8")
    assert 'FOOBAR' in data
    assert "2" in data


def test_add_new_student(client, ctx):
    url_from = url_for("add_new_student")
    resp = client.get(url_from)
    assert resp.status_code == 200

    url_to = url_for("add_student")
    response = client.post(url_to, data={
        "first_name": "Joseph",
        "last_name": "Gach",
        "group_id": "200",
    })
    assert response.status_code == 200
    data = response.data.decode("utf-8")
    assert "COOL" in data


def test_show_courses(client, ctx):
    url = url_for("show_courses", id="1", delete_from_course="15")
    resp = client.get(url)
    data = resp.data.decode("utf-8")
    assert resp.status_code == 200
    assert "FOO" in data
    assert "BAR" in data
    assert resp.request.args.get("delete_from_course") == "15"

    url = url_for("show_courses", id="3", course_id="15")
    resp = client.get(url)
    data = resp.data.decode("utf-8")
    assert "foo" in data
    assert "bar" in data
    assert resp.request.args.get("course_id") == "15"


def test_show_all_courses(client, ctx):
    url = url_for("show_all_courses")
    resp = client.get(url)
    url1 = url_for('all_students', course=15)
    url2 = url_for('all_students', course=25)
    url3 = url_for('all_students', course=35)
    url4 = url_for('all_students', course=36)
    data = resp.data.decode("utf-8")
    assert url1 in data
    assert url2 in data
    assert url3 in data
    assert url4 in data


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
