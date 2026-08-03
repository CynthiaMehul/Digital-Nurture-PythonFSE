import {Routes, Route} from 'react-router-dom'
import Home from './components/Home'
import CoursePage from './components/CoursesPage'
import ProfilePage from './components/ProfilePage'
import CourseDetailPage from './components/CourseDetailPage'
// import {EnrollmentProvider} from './context/EnrollmentContext'
import Header from './components/Header'

import { Provider } from "react-redux";
import { store } from "./redux/store";

function App() {
  return (
    <>
    {/* <EnrollmentProvider> */}
    <Provider store={store}>
      <Header/>
      <Routes>
        <Route path='/' element={<Home/>}/>
        <Route path='/courses' element={<CoursePage/>}/>
        <Route path='/profile' element={<ProfilePage/>}/>
        <Route path='/courses/:courseId' element={<CourseDetailPage/>}/>
      </Routes>
     </Provider>
     {/* </EnrollmentProvider> */}
    </>
  )
}

export default App
