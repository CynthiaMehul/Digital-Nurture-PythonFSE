import {Link} from 'react-router-dom'
import {useContext} from 'react'
// import { EnrollmentContext } from '../context/EnrollmentContext'
import { useSelector } from "react-redux";

function Header(){
    // const {enrolledCourses}=useContext(EnrollmentContext)
    const enrolledCourses=useSelector(state=>state.enrollment.enrolledCourses)
    return (
        <div>
            <h2>Student Portal</h2>
            <Link to='/'>Home</Link>
            <Link to='/courses'>Courses</Link>
            <Link to='/profile'>Profile</Link>
            <br/>
            <h4>Enrolled Course Count: {enrolledCourses.length}</h4>
        </div>
    )
}
 
export default Header