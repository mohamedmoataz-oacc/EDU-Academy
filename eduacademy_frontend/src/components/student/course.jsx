import React from 'react';
import purple from "../Assets/books.png";
import { useNavigate } from "react-router-dom";

export const Course = ({course_title, teacher, thumbnail, enrolled_Date}) => {

  return (
    <div className='course'>
        <div className='course-info'>
            <h1>{course_title}</h1>
            <h3>Teacher: {teacher}</h3>
            <p>Enrolled on: {enrolled_Date}</p>
        </div>
        <div className='course-thumbnail'>
          <img src={thumbnail} alt="Course image"></img>
          {/*<img src={URL.createObjectURL(thumbnail)} alt="Course image"></img>*/}
          <button>Continue Learning</button>
          {/*onClick={() =>{
            navigate("/lectures")
          }}*/}
        </div>
    </div>
  )
}
