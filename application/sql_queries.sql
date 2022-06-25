--Find all groups with less or equals student count.

SELECT groups.name, COUNT(students.group_id)
FROM groups INNER JOIN students ON groups.id = students.group_id
GROUP BY groups.id
HAVING COUNT(students.group_id) = (
	SELECT COUNT(students.group_id)
	FROM groups INNER JOIN students ON groups.id = students.group_id
	GROUP BY groups.id
	ORDER BY COUNT(students.group_id)
	LIMIT 1)
ORDER BY COUNT(students.group_id)


--Find all students related to the course with a given name.

SELECT students.first_name, students.last_name
FROM students
INNER JOIN student_course_assoc ON students.id = student_course_assoc.student_id
INNER JOIN courses ON student_course_assoc.course_id = courses.id
WHERE courses.name = 'Biology'
ORDER BY students.last_name

--Add new student

INSERT INTO students (first_name, last_name, group_id) VALUES ('Eugene', 'The best', 1)

--Delete student by STUDENT_ID
DELETE FROM student_course_assoc
WHERE student_course_assoc.student_id = 3;
DELETE FROM students
WHERE students.id = 3;

--Add a student to the course

INSERT INTO student_course_assoc (student_id, course_id) VALUES (2, 10)

--Remove the student from one of his or her courses

DELETE  FROM student_course_assoc
WHERE student_id = 2 AND course_id = 10