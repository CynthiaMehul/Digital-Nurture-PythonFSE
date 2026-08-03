import courses from '../data/data.js'
import {useContext} from 'react'
import {useNavigate, useParams} from 'react-router-dom'
// import { EnrollmentContext } from '../context/EnrollmentContext.jsx'
import {enroll} from '../redux/enrollmentSlice.js'
import { useDispatch } from "react-redux";

function CourseDetailPage(){
    const {courseId}=useParams()
    const course=courses.filter((course)=>course.id==courseId)
    const navigate=useNavigate()
    // const {enrolledCourses, setEnrolledCourses}=useContext(EnrollmentContext)
    const dispatch=useDispatch()

    return (
        <>
            <h1>Course Detail Page</h1>
            <h3>Course ID: {course[0].id}</h3>
            <h3>Course Name: {course[0].name}</h3>
            <h4>Credits: {course[0].credits}</h4>
            <p>Grade: {course[0].grade}</p>
            <br/>
            {/* <button onClick={()=>{
                console.log([...enrolledCourses,course[0]])
                setEnrolledCourses((prev) => [...prev,course[0]])
                navigate('/profile')}}>Enroll</button> */}

            <button onClick={()=>{dispatch(enroll(course[0]))}}>Enroll</button>
        </>

    )
}

export default CourseDetailPage