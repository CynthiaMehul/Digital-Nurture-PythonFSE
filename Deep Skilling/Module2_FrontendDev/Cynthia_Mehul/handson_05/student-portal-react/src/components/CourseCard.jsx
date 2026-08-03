function CourseCard(props){
    return (
        <div style={{backgroundColor:"pink"}}>
            <h3>{props.name}</h3>
            <h4>{props.code}</h4>
            <p>Credits: {props.credits}</p>
            <p>Grade: {props.grade}</p>
            <br/>
            <button onClick={props.onEnroll}>Enroll</button>
        </div>
    )
}
export default CourseCard