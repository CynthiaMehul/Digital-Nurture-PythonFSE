import courses from './data.js'

let courseGrid=document.querySelector('.course-grid');
function renderCourses(courses){
    for(let i=0;i<courses.length;i++){
        const articleElement=document.createElement("article");
        articleElement.className="course-card";
        articleElement.dataset.name=courses[i].name;
        articleElement.dataset.grade=courses[i].grade;
        articleElement.innerHTML=`
            <h3>${courses[i].code}</h3>
            <h4>${courses[i].name}</h4>
            <p>Credits: ${courses[i].credits}<p>
        `
        courseGrid.append(articleElement);
    }
}
// TASK 1

const formattedCourses=courses.map((course)=>{
    return `${course.code} - ${course.name} (${course.credits} credits)`
});

console.log("Fomatted Courses:");

// for(let i=0;i<courses.length;i++){
//     console.log(formattedCourses[i])
// }

formattedCourses.forEach(course=>console.log(course));

const filteredCourses=courses.filter((course)=>{
    return course.credits>=4
});

console.log("\nNumber of Courses with Credits Greater than 4:",filteredCourses.length);

const totalCredits=courses.reduce((acc,course)=>{
    return acc+course.credits
},0);

console.log("\nTotal Number of Credits:",totalCredits);

// TASK 2

renderCourses(courses)

const creditTag=document.getElementById("credits")
creditTag.innerText=`Credits: ${totalCredits}`

// TASK 3

const searchInput=document.getElementById("search-courses");

searchInput.addEventListener("input", (event)=>{
    const searchValue=event.target.value.toLowerCase()
    let renderedCourse=courses.filter((course)=>{
        return course.name.toLowerCase().startsWith(searchValue)
    })

    courseGrid.innerHTML="";
    renderCourses(renderedCourse)
});

function sortButton(){
    courseGrid.innerHTML="";
    let renderedCourse=courses.sort((a,b)=>b.credits-a.credits);

    renderCourses(renderedCourse)
}

const sortBtn = document.getElementById("sort-button")

sortBtn.addEventListener("click",sortButton);

courseGrid.addEventListener("click",(event)=>{
    const card = event.target.closest(".course-card")
    alert(`
        Course Name: ${card.dataset.name}
        Grade: ${card.dataset.grade}
    `)
})