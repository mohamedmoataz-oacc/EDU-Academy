import React from 'react'
import { Courses } from './Courses';
import books from '../Assets/books.png';



export const Home = (courses) => {

  return (
    <>
    <div className='teacherp '>
        <div className='great user-container'><h1>Welcome back !</h1>
         <p>
        Your commitment to education is truly commendable.
        Your influence extends far beyond the classroom,<br></br>
        shaping the minds of future leaders and innovators.
        </p>
        </div>
    </div>
       {courses.length === 0 ? <></> :
        (
       <div className='courses'>
        <h1>My courses</h1>
        <div className='st'>
            {courses.map((course, index) => (
              <Courses
                key={index}
                course_name={course.course_name}
                thumbnail={course.thumbnail}
                subject={course.subject}
                teacher_name={course.teacher_name}
                assisting_date={course.assisting_date}
                course_description={course.course_description}
                is_completed={course.is_completed}
              />
            ))}
            </div>
        </div>
        )}

    
    </>
  )
  
}
