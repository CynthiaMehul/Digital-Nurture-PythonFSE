import Header from "./Header"
// import {EnrollmentContext} from "../context/EnrollmentContext.jsx"
// import {useContext} from 'react'
import { unenroll } from "../redux/enrollmentSlice.js"
import { useDispatch, useSelector } from 'react-redux'

function ProfilePage(){
    // const {enrolledCourses, unEnroll} = useContext(EnrollmentContext)
    const enrolledCourses=useSelector((state)=>state.enrollment.enrolledCourses)
    const dispatch=useDispatch()
    return (
        <div>
            Profile Page
            {
                enrolledCourses.map((course)=>{
                    return (
                        <div key={course.id}>
                            <h3>Course ID: {course.id}</h3>
                            <h3>Course Name: {course.name}</h3>
                            <h4>Credits: {course.credits}</h4>
                            <p>Grade: {course.grade}</p>
                            <br/>
                            <button onClick={()=>dispatch(unenroll(course.id))}>Un-Enroll</button>
                        </div>
                    )
                })
            }
        </div>
    )
}
 
export default ProfilePage