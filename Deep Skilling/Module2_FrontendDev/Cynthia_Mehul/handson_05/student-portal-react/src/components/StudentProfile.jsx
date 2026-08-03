import {useState} from 'react'

function StudentProfile(){
    const [name,setName]=useState("")
    const [email,setEmail]=useState("")
    const [semester,setSemester]=useState("")

    return (
        <>  
            <h1>Student Detail Form:</h1>
            <label>Name:</label>
            <input type="text" placeholder="Enter Name" onChange={()=>setName(event.target.value)} value={name} />
            <label>Email:</label>
            <input type="email" placeholder="Enter Email" onChange={()=>setEmail(event.target.value)} value={email} />
            <label>Semester:</label>
            <input type="number" placeholder="Enter Semester" onChange={()=>setSemester(event.target.value)} value={semester} />

        </>
    )
}

export default StudentProfile