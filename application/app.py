import os

from sqlalchemy.orm import sessionmaker
from application import app, Base, engine

from flask import url_for, request, jsonify, Response
from flask_restful import Api, Resource

from flasgger import Swagger, swag_from

from json2xml import json2xml
import trafaret as t

from .database import crud

TO_XML = "xml"
PATH_TO_YML = "swagger_files"

app.config['DEBUG'] = True


SessionLocal = sessionmaker()
Base.metadata.bind = engine

SessionLocal.configure(bind=engine)
session = SessionLocal()


api = Api(app, catch_all_404s=True, prefix="/api/v1")
swagger = Swagger(app)


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
        t.String().check(f)
        l = str(args["lastname"])
        t.String().check(l)
        g = int(args["group_id"])
        t.Int().check(g)
        crud.add_new_student(db=session, first=f, last=l, group=g)
        return jsonify({"message": "Successfully added"})

    @swag_from(os.path.join(PATH_TO_YML, "delete_student.yml"))
    def delete(self):
        args = request.args.get("delete_by_id")
        result = crud.delete_student(db=session, student_id=int(args))
        return jsonify(result)


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

    def post(self):
        args = request.get_json()
        n = str(args["name"])
        t.String().check(n)
        d = str(args["description"])
        t.String().check(d)
        result = crud.add_new_course(db=session, course_name=n, description=d)
        return jsonify(result)

    def delete(self):
        group_id = int(request.args.get("group_id"))
        t.Int().check(group_id)
        result = crud.delete_group(db=session, group_id=group_id)
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

    def post(self):
        name_group = request.args.get("group_name")
        t.String().check(name_group)
        result = crud.add_new_group(db=session, group_name=name_group)
        return jsonify(result)

    def delete(self):
        group_id = int(request.args.get("group_id"))
        t.Int().check(group_id)
        result = crud.delete_group(db=session, group_id=group_id)
        return jsonify(result)



class StudentCourse(Resource):
    @swag_from(os.path.join(PATH_TO_YML, "student_courses_get.yml"))
    def get(self):
        format_output = request.args.get("format")
        student_id = request.args.get("student_id")
        result = crud.get_student_course(db=session, student_id=int(student_id))
        if student_id:
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
        t.Int().check(student_id)
        t.Int().check(course_id)
        course = crud.get_course(db=session, course_id=course_id)
        if not course:
            return jsonify({"message": "Course does not exist"})
        student = crud.get_student_course(db=session, student_id=student_id)
        student_courses = [courses.id for courses in student.course]
        if course_id in student_courses:
            return jsonify({"message": "Student is already on it"})
        crud.add_student_to_course(db=session, user_id=student_id, course_id=course_id)
        return jsonify({"message": "Successfully added"})

    @swag_from(os.path.join(PATH_TO_YML, "student_courses_delete.yml"))
    def delete(self):
        student_id = int(request.args.get("student_id"))
        course_id = int(request.args.get("course_id"))
        result = crud.remove_from_course(db=session, course_id=course_id, student_id=student_id)
        return jsonify(result)


api.add_resource(AllStudents, "/students")
api.add_resource(AllCourses, "/courses")
api.add_resource(AllGroups, "/groups")
api.add_resource(StudentCourse, "/student_courses")
api.init_app(app)


if __name__ == '__main__':
    app.run(debug=True)