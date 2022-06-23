DROP TABLE IF EXISTS groups, students, courses, student_courses CASCADE;

CREATE TABLE groups ( id serial PRIMARY KEY, name text);

CREATE TABLE students (
id serial PRIMARY KEY,
first_name varchar,
last_name varchar,
group_id integer REFERENCES groups(id));

CREATE TABLE courses ( id  serial PRIMARY KEY, name  varchar, description varchar);

CREATE TABLE student_course_assoc (
student_id   integer REFERENCES students(student_id) ON DELETE CASCADE,
course_id integer REFERENCES courses(course_id) ON DELETE CASCADE);