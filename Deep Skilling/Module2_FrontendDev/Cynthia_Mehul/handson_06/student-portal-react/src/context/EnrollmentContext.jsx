import {createContext, useState} from 'react'

export const EnrollmentContext=createContext()

export function EnrollmentProvider(props){
    const [enrolledCourses,setEnrolledCourses]=useState([])
    function unEnroll(id){
        const newEnrolledCourses=enrolledCourses.filter((course)=>{
            return course.id!=id
        })
        setEnrolledCourses(newEnrolledCourses)
    }
    return (
        <EnrollmentContext.Provider value={{enrolledCourses: enrolledCourses,setEnrolledCourses: setEnrolledCourses, unEnroll: unEnroll}}>
            {props.children}
        </EnrollmentContext.Provider>
    )
}

