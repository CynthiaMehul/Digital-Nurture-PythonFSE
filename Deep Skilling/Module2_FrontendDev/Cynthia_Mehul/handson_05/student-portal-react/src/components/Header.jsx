function Header(props){
    return (
        <div>
            <h1>{props.siteName}</h1>
            <a href="#">Home</a>
            <a href="#">Courses</a>
            <a href="#">Profile</a>
            <br/>
            <h2>Courses Enrolled: {props.courseCount}</h2>
        </div>
    )
}
export default Header