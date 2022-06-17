import os

from application import app

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from flask import render_template, url_for, request, jsonify, Response
from flask_restful import Api, Resource

from flasgger import Swagger, swag_from

from json2xml import json2xml

from database import crud
from database.db import Base

TO_XML = "xml"
PATH_TO_YML = "swagger_files"

engine = create_engine(app.config["SQLALCHEMY_DATABASE_URI"])
Base.metadata.bind = engine

DBSession = sessionmaker(engine)
session = DBSession()

api = Api(app, catch_all_404s=True, prefix="/api/v1")
swagger = Swagger(app)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/all_students/", methods=["GET"])
def all_students():
    course = request.args.get("course")
    if course:
        course = int(course)
    if request.args.get("delete_students"):
        crud.delete_student(db=session, student_id=int(request.args.get("delete_students")))
    return render_template("all_students.html", result=crud.get_all_(db=session, course_id=course))


@app.route("/the_smallest_group/")
def smallest_group():
    all_group = request.args.get("all")
    return render_template("the_smallest_group.html", result=crud.get_groups(db=session, all=all_group))


@app.route("/add_new_student/")
def add_new_student():
    return render_template("add_new_students.html")


@app.route("/new_student/", methods=["GET", "POST"])
def add_student():
    if request.method == "POST":
        first = request.form.get("first_name")
        last = request.form.get("last_name")
        group = request.form.get("group_id")
        crud.add_new_student(db=session, first=first, last=last, group=group)
        return render_template("new_student.html")
    return render_template("add_new_students.html")


@app.route("/student_courses/")
def show_courses():
    student_id = int(request.args.get("id"))
    delete_from_course = request.args.get("delete_from_course")
    course_id = request.args.get("course_id")
    if delete_from_course:
        crud.remove_from_course(
            db=session, student_id=student_id, course_id=int(delete_from_course))
    elif course_id:
        crud.add_student_to_course(db=session, user_id=student_id, course_id=int(course_id))
    return render_template("show_courses.html", result=crud.get_students_course(db=session, student_id=student_id),
                           all_courses=crud.get_courses(db=session))


@app.route("/courses/")
def show_all_courses():
    return render_template("courses.html", result=crud.get_courses(db=session))


class AllStudents(Resource):

    @swag_from(os.path.join(PATH_TO_YML, "student_get.yml"))
    def get(self):
        format_output = request.args.get("format")
        course = request.args.get("course_id")
        result = crud.get_all_(db=session, course_id=course)
        result = {index: {
            "student id": student.id,
            "first name": student.first_name,
            "last name": student.last_name,
            "group_id": student.group_id,
        } for index, student in enumerate(result, 1)}
        if format_output == TO_XML:
            return Response(json2xml.Json2xml(result).to_xml(), mimetype="txt/xml")
        return jsonify(result)

    @swag_from(os.path.join(PATH_TO_YML, "students_post.yml"))
    def post(self):
        args = request.get_json()
        f = str(args["firstname"])
        l = str(args["lastname"])
        g = int(args["group_id"])
        crud.add_new_student(db=session, first=f, last=l, group=g)
        return jsonify({"message": "Successfully added"})

    @swag_from(os.path.join(PATH_TO_YML, "delete_student.yml"))
    def delete(self):
        args = request.args.get("delete_by_id")
        crud.delete_student(db=session, student_id=int(args))
        return jsonify({"message": "Successfully deleted"})


class AllCourses(Resource):
    @swag_from(os.path.join(PATH_TO_YML, "course_get.yml"))
    def get(self):
        format_output = request.args.get("format")
        result = crud.get_courses(db=session)
        result = {course.id: {
            "name": course.name,
            "description": course.description,
            "student`s count": len(course.student)
        } for course in result}
        if format_output == TO_XML:
            return Response(json2xml.Json2xml(result).to_xml(), mimetype="txt/xml")
        return jsonify(result)


class AllGroups(Resource):
    @swag_from(os.path.join(PATH_TO_YML, "group_get.yml"))
    def get(self):
        format_output = request.args.get("format")
        result = crud.get_groups(db=session, all=True)
        result = {index: {
            "name": group.name,
            "students count": group[0]
        } for index, group in enumerate(result, 1)}
        if format_output == TO_XML:
            return Response(json2xml.Json2xml(result).to_xml(), mimetype="txt/xml")
        return jsonify(result)


class StudentCourse(Resource):
    @swag_from(os.path.join(PATH_TO_YML, "student_courses_get.yml"))
    def get(self):
        format_output = request.args.get("format")
        student_id = request.args.get("student_id")
        result = crud.get_students_course(db=session, student_id=int(student_id))
        result = {
            "Firstname": result.first_name,
            "Lastname": result.last_name,
            "Group_id": result.group_id,
            "Courses": {index: {
                "name": courses.name,
                "id": courses.id
            } for index, courses in enumerate(result.course, 1)}}
        if format_output == TO_XML:
            return Response(json2xml.Json2xml(result).to_xml(), mimetype="txt/xml")
        return jsonify(result)

    @swag_from(os.path.join(PATH_TO_YML, "student_courses_post.yml"))
    def post(self):
        student_id = int(request.args.get("student_id"))
        course_id = int(request.args.get("course_id"))
        all_courses = crud.get_courses(db=session)
        courses = [courses.id for courses in all_courses]
        student = crud.get_students_course(db=session, student_id=student_id)
        student_courses = [courses.id for courses in student.course]
        if course_id not in courses:
            return jsonify({"message": "Course does not exist"})
        elif course_id in student_courses:
            return jsonify({"message": "Student is already on it"})
        crud.add_student_to_course(db=session, user_id=student_id, course_id=course_id)
        return jsonify({"message": "Successfully added"})

    @swag_from(os.path.join(PATH_TO_YML, "student_courses_delete.yml"))
    def delete(self):
        student_id = int(request.args.get("student_id"))
        course_id = int(request.args.get("course_id"))
        crud.remove_from_course(db=session, course_id=course_id, student_id=student_id)
        return jsonify({"message": "Successfully deleted"})


api.add_resource(AllStudents, "/students")
api.add_resource(AllCourses, "/courses")
api.add_resource(AllGroups, "/groups")
api.add_resource(StudentCourse, "/student_courses")
api.init_app(app)


if __name__ == '__main__':
    app.run(debug=True)