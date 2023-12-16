import React from 'react';
import { FaArrowRightLong } from "react-icons/fa6";
import { useNavigate } from "react-router-dom";



export const Lecture = () => {
    const navigate = useNavigate();
  const lecture ={
    lecture_title: "Quantum physics",
    about: "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."
  }
  return (
    <div className='lecture'>
        <div>
            <h2>{lecture.lecture_title}</h2>
            {lecture.about}
        </div>
        <div>
            <button onClick={() =>{
              navigate("/lecture")
             }
            }><FaArrowRightLong /></button>
        </div>
    </div>

  )
}