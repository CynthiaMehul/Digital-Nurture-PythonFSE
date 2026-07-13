import { courses } from "./data.js";

courses.forEach(course => {
    const { name, credits } = course;
    console.log(`${name} - ${credits} credits`);
});

const formattedCourses = courses.map(
    course => `${course.code} — ${course.name} (${course.credits} credits)`
);

console.log(formattedCourses);

const filteredCourses = courses.filter(course => course.credits >= 4);

console.log("Courses with >=4 credits:", filteredCourses.length);

const totalCredits = courses.reduce(
    (sum, course) => sum + course.credits,
    0
);

console.log("Total Credits:", totalCredits);

const courseGrid = document.querySelector(".course-grid");
const total = document.getElementById("total-credits");
const search = document.getElementById("search-courses");
const sortBtn = document.getElementById("sort-btn");
const selected = document.getElementById("selected-course");

let currentCourses = [...courses];

function renderCourses(courseList){

    courseGrid.innerHTML = "";

    courseList.forEach(course => {

        const card = document.createElement("article");

        card.className = "course-card";

        card.dataset.id = course.id;

        card.innerHTML = `
            <h3>${course.name}</h3>
            <p>${course.code}</p>
            <span>Credits: ${course.credits}</span>
        `;

        courseGrid.appendChild(card);

    });

    const totalCredits = courseList.reduce(
        (sum, course) => sum + course.credits,
        0
    );

    total.textContent = `Total Credits: ${totalCredits}`;
}

renderCourses(currentCourses);


search.addEventListener("input", () => {

    const value = search.value.toLowerCase();

    const filtered = currentCourses.filter(course =>
        course.name.toLowerCase().includes(value)
    );

    renderCourses(filtered);

});


sortBtn.addEventListener("click", () => {

    currentCourses.sort((a,b)=>b.credits-a.credits);

    renderCourses(currentCourses);

});


courseGrid.addEventListener("click",(event)=>{

    const card = event.target.closest(".course-card");

    if(!card) return;

    const id = Number(card.dataset.id);

    const course = courses.find(c=>c.id===id);

    selected.textContent =
    `Selected Course: ${course.name} | Grade: ${course.grade}`;

});