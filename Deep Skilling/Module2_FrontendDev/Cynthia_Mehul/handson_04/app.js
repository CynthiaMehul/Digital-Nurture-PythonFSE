import courses from './data.js'

// step 45
function fetchUser1(id){
    return fetch(`https://jsonplaceholder.typicode.com/users/${id}`)
}

fetchUser1(1).then(response=>response.json())
.then(user=>{console.log(user.name)})

// step 46
async function fetchUser2(id){
    try{
        const response = await fetch(`https://jsonplaceholder.typicode.com/users/${id}`)
        const userData = await response.json()
        console.log(userData.name)
    }
    catch(error){
        console.log(error)
    }
}

fetchUser2(1)


// step 47
function fetchAllCourses(){
    const fetchCourses=new Promise(resolve=>setTimeout(()=>resolve(courses),1000))
    return fetchCourses
}

fetchAllCourses().then((courses)=>{console.log(courses)})


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

// step 48

async function asyncRenderCourses(){
    const loadingElement = "<p>Loading courses...</p>"
    courseGrid.innerHTML = loadingElement;
    const courses=await fetchAllCourses()
    courseGrid.innerHTML = ''
    renderCourses(courses)
}

asyncRenderCourses()

const creditTag=document.getElementById("credits")
creditTag.innerText=`Credits: ${totalCredits}`


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


// step 49
const promise1=fetchUser1(1).then(response=>response.json())
const promise2=fetchUser1(2).then(response=>response.json())
Promise.all([promise1,promise2]).then((promises)=>{console.log(promises)})


// step 50

async function apiFetch(url){
    try{
        const response = await fetch(url)
        if (!response.ok){
            throw new Error("Error while fetching user data")
        }
        const userData = await response.json()
        console.log(userData.name)
        return userData
    }
    catch(error){
        console.log(error.name)
        console.log(error.message)
    }
}

//apiFetch(`https://jsonplaceholder.typicode.com/users/1000000000`)

// step 51

const notifsGrid=document.querySelector('.notification-grid')
async function renderNotifs(){
    const notifs=await apiFetch(`https://jsonplaceholder.typicode.com/posts`)
    for(let i=0;i<6;i++){
        const divElement=document.createElement("div");
        divElement.className="course-card";
        divElement.innerHTML=`
            <h3>${notifs[i].id}</h3>
            <h4>${notifs[i].title}</h4>
            <p>Content: ${notifs[i].body}<p>
        `
        notifsGrid.append(divElement);
    }
}

//renderNotifs()

// step 52

async function renderNotifsLoading(){
    const loadingElement = "<img src='https://supersimple.dev/images/loading-spinner.gif' style={{ height: '40px', margin: '-15px' }}/>"
    notifsGrid.innerHTML=loadingElement
    try{
        const notifs=await apiFetch(`https://jsonplaceholder.typicode.com/100000`)
        notifsGrid.innerHTML=''
        for(let i=0;i<6;i++){
            const divElement=document.createElement("div");
            divElement.className="course-card";
            divElement.innerHTML=`
                <h3>${notifs[i].id}</h3>
                <h4>${notifs[i].title}</h4>
                <p>Content: ${notifs[i].body}<p>
            `
            notifsGrid.append(divElement);
        }
    }
    catch(error){
        // step 53
        const errorElement="<p>Failed to fetch notifications</p>"
        const retryButton=`<br><button class='retry-button'>retry</button>`
        notifsGrid.innerHTML=errorElement+retryButton
        const button=document.querySelector('.retry-button')
        button.addEventListener("click",retryButtonRender)
    }
}

// step 54
async function retryButtonRender(){
    const loadingElement = "<img src='https://supersimple.dev/images/loading-spinner.gif' style={{ height: '40px', margin: '-15px' }}/>"
    notifsGrid.innerHTML=loadingElement
    const notifs=await apiFetch(`https://jsonplaceholder.typicode.com/posts`)
    notifsGrid.innerHTML=''
    for(let i=0;i<6;i++){
        const divElement=document.createElement("div");
        divElement.className="course-card";
        divElement.innerHTML=`
            <h3>${notifs[i].id}</h3>
            <h4>${notifs[i].title}</h4>
            <p>Content: ${notifs[i].body}<p>
        `
        notifsGrid.append(divElement);
    }
}

renderNotifsLoading()

// step 58

const api = axios.create({
  baseURL: 'https://jsonplaceholder.typicode.com'
});

api.interceptors.request.use(
  (config) => {
    console.log(`API call started: ${config.baseURL+config.url}`)
    return config;
  },
  (error) => Promise.reject(error)
);

// step 56

async function apiFetchAxios(url){
    const response=await api.get(url)
    console.log(response.data)
}

apiFetchAxios('/users/1')

// step 57

async function apiFetchAxiosParams(){
    const response=await api.get('/posts', { params: { userId: 1 } })
    console.log(response.data)
}

apiFetchAxiosParams()


// step 59

/*
Fetch vs Axios

1. JSON Handling:
   - Fetch: Must manually call response.json().
   - Axios: Automatically parses JSON responses.

2. Error Handling:
   - Fetch: Only rejects on network errors; check response.ok for HTTP errors.
   - Axios: Automatically rejects for HTTP error status codes (4xx, 5xx).

3. Features:
   - Fetch: Built into modern browsers; no installation required.
   - Axios: External library that supports request/response interceptors, automatic timeouts, and request cancellation.
*/




