import React from 'react'
import { Course } from './course'

export const MyCourses = () => {
  const data = {
    fname:"",
    lname:"",
    img:"",
    academicYear: "",
    points:""
  } 
  return (
    <div className='courses'>
        <div className='user-container'>
            <div className='user'>
                <div>
                    <h1>Hi {data.fname},</h1>
                Welcome to a world of endless possibilities!<br /> Your learning journey is a key to unlocking your full potential. 
                Embrace each lesson with enthusiasm, as every step forward brings you closer to your dreams.
                </div>
                <button className='continue'>Continue Learning</button>
            </div>
            <div className='points'>
                <h6>Good Job!</h6>
                <h4>You've earned</h4>
                <h1>{data.points}</h1>
                <h3>Points</h3>
                <div></div>
            </div>
        </div>
        <h1>MY COURSES</h1>
    </div>
  )
}

