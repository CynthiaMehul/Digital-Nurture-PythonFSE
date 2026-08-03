import Header from './components/Header.jsx'
import Footer from './components/Footer.jsx'
import CourseCard from './components/CourseCard.jsx'
import {useState, useEffect} from 'react'
import courses from './data/data.js'
import StudentProfile from './components/StudentProfile.jsx'


function App() {
  const [course,setCourses]=useState([])
  const [searchTerm,setSearchTerm]=useState("")
  const [enrolledCourses,setEnrolledCourses]=useState([])
  const [loading,setLoading]=useState(true)
  const [error,setError]=useState("")

  useEffect(()=>console.log(enrolledCourses),[enrolledCourses])

  useEffect(()=>{
    fetch("https://jsonplaceholder.typicode.com/posts")
      .then(response=>{
        if(response.ok) return response.json()
        else throw new Error("Error while fetching data")
    })
        .then(data=>{
          setCourses(data)
        })
          .catch((error)=>{
            setError(error.message)
          })
            .finally(()=>setLoading(false))
  },[])
  const handleEnroll=(course)=>setEnrolledCourses([...enrolledCourses,course])
 
  let filteredCourses=(searchTerm=="")?courses:
          courses.filter((course)=>course.name.toLowerCase().startsWith(searchTerm.toLowerCase()))

  
  return (
    <>
        <Header siteName="Student Portal" courseCount={enrolledCourses.length}/>

        <input type='text' placeholder="Search Courses" onChange={(event)=>setSearchTerm(event.target.value)} value={searchTerm}/>

        {error && <h2>{error}</h2>}
        {
          (loading)? <h2>Loading...</h2>:course.slice(0,5)
          .map((course)=>{
            return (
              <div key={course.id}>
                <h2>{course.id}</h2>
                <h3>{course.title}</h3>
                <p>{course.body}</p>
              </div>
            )
          })
        }

       
         {filteredCourses.map((course)=>{ return (
           <CourseCard key={course.id} name={course.name} code={course.code} credits={course.credits} 
                   grade={course.grade} onEnroll={()=>handleEnroll(course)}/>
         )})}
         

        <StudentProfile/>
        <Footer/>
    </>
  )
}
export default App
