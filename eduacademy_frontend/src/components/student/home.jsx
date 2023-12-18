import React from 'react'
import { Course } from './course'

export const MyCourses = (myCourses, courses, data) => {

 {/* const data = {
    fname,
    points
  } */}
  
  return (
    <div className='my-learning'>
        <div className='user-container'>
            <div className='user'>
                <div>
                    <h1>Hi {data.fname},</h1>
                Welcome to a world of endless possibilities!<br /> Your learning journey is a key to unlocking your full potential. 
                Embrace each lesson with enthusiasm, as every step forward brings you closer to your dreams.
                </div>
            </div>
            <div className='points'>
                <h6>Good Job!</h6>
                <h4>You've earned</h4>
                <h1>{data.points}</h1>
                <h3>Points</h3>
                <div></div>
            </div>
            {/*
          <button className='continue'>Continue Learning</button> */}

        </div>

        {myCourses.length === 0 ? <></> :
        (
          <div className='courses'>
            <h1>MY COURSES</h1>
            <div className='st'>
            {myCourses.map((course, index) => (
              <Course
                key={index}
                course_title={course.course_title}
                teacher={course.teacher}
                thumbnail={course.thumbnail}
                enrolled_Date={course.enrolled_Date}
              />
            ))}
            </div>
          </div>
        )}

        <div className='courses'>
        <h1>Other courses</h1>
        <div className='st'>
            {courses.map((course, index) => (
              <Courses
                key={index}
                course_title={course.course_title}
                teacher={course.teacher}
                thumbnail={course.thumbnail}
                enrolled_Date={course.enrolled_Date}
              />
            ))}
            </div>
        </div>

        
    </div>
  )
}

