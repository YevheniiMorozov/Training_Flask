--Find all groups with less or equals student count.
SELECT top 1 groups.name
FROM group INNER JOIN student_course_assoc ON groups.id = student_course_assoc.group_id
ORDER BY count(student_course_assoc.group_id)
GROUP BY student_course_assoc.group_id

--Find all students related to the course with a given name.

SELECT students.first_name, students.last_name
FROM students
WHERE students.groups.name = "name"
ORDER BY students.last_name

--Add new student

INSERT INTO students (first_name, last_name, group_id) VALUES ('Eugene', 'The best', 1)

--Delete student by STUDENT_ID

DELETE * FROM students
WHERE students.id = 3

--Add a student to the course

INSERT INTO student_course_assoc (student_id, course_id) VALUES (2, 10)

--Remove the student from one of his or her courses

DELETE * FROM student_course_assoc
WHERE student_id = 2, course_id = 10