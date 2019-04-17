-- 4.1
select Name from HW11_students where CWID='11461';

--4.2
select Major, count(*) as Count  From
HW11_students stu
group by Major;

--4.3
select Grade from
    (select Grade, count(Grade) as occurences from HW11_grades
order by occurences DESC limit 1);

--4.3 alt?
select Grade, count(*) as cnt from HW11_grades
group by Grade order by cnt desc limit 1;

--4.4
select s.Name, s.CWID, s.Major, g.Course, g.Grade
from HW11_students as s
    join HW11_grades as g on s.CWID=g.Student_CWID;

--4.5
select s.Name
from HW11_students as s
    join HW11_grades as g on s.CWID=g.Student_CWID
where g.Course='SSW 540';

--4.6
-- select i.CWID, i.Name, i.Dept, g.Course, g.Student_CWID
select i.cwid, i.name, i.Dept, g.course, count(*) as students
from HW11_instructors as i
    join HW11_grades as g on i.CWID=g.Instructor_CWID
group by i.cwid, g.course order by i.CWID desc;