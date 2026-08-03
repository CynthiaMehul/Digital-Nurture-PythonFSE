import courses from '../data/data.js'
import {useContext} from 'react'
// import { EnrollmentContext } from '../context/EnrollmentContext.jsx'
import { useDispatch } from 'react-redux'
import {enroll} from '../redux/enrollmentSlice.js'

function CoursesPage(){
    // const {enrolledCourses, setEnrolledCourses}=useContext(EnrollmentContext)
    const dispatch=useDispatch()
    return (
        <>
        <h1>Courses Page</h1>
        {courses.map((course) => {
            return (
            <div key={course.id}>
                <h3>Course ID: {course.id}</h3>
                <h3>Course Name: {course.name}</h3>
                <h4>Credits: {course.credits}</h4>
                <p>Grade: {course.grade}</p>
                <br/>
                <button onClick={()=>{
                    dispatch(enroll(course))}}>Enroll</button>
            </div>
            )
        })}
        </>

    )
}

export default CoursesPage