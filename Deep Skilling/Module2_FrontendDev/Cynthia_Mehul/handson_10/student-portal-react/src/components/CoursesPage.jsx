import { useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";

import { enroll } from "../redux/enrollmentSlice.js";

import {
  fetchAllCourses,
  selectCourses,
  selectCoursesLoading,
  selectCoursesError,
} from "../redux/coursesSlice.js";

function CoursesPage() {
  const dispatch = useDispatch();

  const courses = useSelector(selectCourses);
  const loading = useSelector(selectCoursesLoading);
  const error = useSelector(selectCoursesError);

  useEffect(() => {
    dispatch(fetchAllCourses());
  }, [dispatch]);

  if (loading) {
    return <h2>Loading courses...</h2>;
  }

  if (error) {
    return <h2>Error: {error}</h2>;
  }

  return (
    <>
      <h1>Courses Page</h1>

      {courses.map((course) => {
        return (
          <div key={course.id}>
            <h3>Course ID: {course.id}</h3>

            <h3>Course Name: {course.title}</h3>

            <p>{course.body}</p>

            <button
              onClick={() => {
                dispatch(enroll(course));
              }}
            >
              Enroll
            </button>

            <br />
            <br />
          </div>
        );
      })}
    </>
  );
}

export default CoursesPage;