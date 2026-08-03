import courses from './data.js';

let courseGrid =
    document.querySelector('.course-grid');

const searchResults =
    document.getElementById("search-results");

function updateSearchResults(count) {
    const courseText =
        count === 1 ? "course" : "courses";

    searchResults.textContent =
        `${count} ${courseText} found`;
}

function renderCourses(courses) {
    for(let i=0;i<courses.length;i++){
        const articleElement=document.createElement("article");
        articleElement.className="course-card";
        articleElement.tabIndex = 0;    
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

    courseGrid.innerHTML = "";
    renderCourses(renderedCourse);
    updateSearchResults(renderedCourse.length);
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

courseGrid.addEventListener("keydown", (event) => {
    if (event.key === "Enter") {
        const card = event.target.closest(".course-card");

        if (card) {
            card.click();
        }
    }
});

const menuButton =
    document.getElementById("menu-toggle");

const mainNavigation =
    document.getElementById("main-navigation");

menuButton.addEventListener("click", () => {
    const isExpanded =
        menuButton.getAttribute("aria-expanded") === "true";

    menuButton.setAttribute(
        "aria-expanded",
        String(!isExpanded)
    );

    mainNavigation.classList.toggle(
        "menu-open"
    );
});

cssVars({
    onlyLegacy: false
});