import React from 'react'
import { MdVerified } from "react-icons/md";


export const Courses = ({course_name,subject, teacher_name, thumbnail, assisting_date, course_description, is_completed}) => {
  return (
    <div className='course'>
        <div className='course-info'>
            <h1>{course_name}{is_completed &&<MdVerified style={{color:'#09af09', cursor:'pointer', padding:'5px 0 0 0'} } title='completed'/>}</h1>
            <p><span className='strong'>Teacher </span>{teacher_name}</p>
            <p><span className='strong'>Subject </span> {subject}</p>
            <p><span className='strong'>Assisting Date </span> {assisting_date}</p>
            <p >{course_description}</p>
        </div>

        <div className='course-thumbnail'>
          <img src={thumbnail} alt="Course image"></img>
          
          <button>check !</button>
          
        </div>
    </div>
  )
}
