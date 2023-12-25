import React, { useState } from 'react';
import { FiUpload } from "react-icons/fi";
import { Courses } from './Courses';
import books from '../Assets/books.png';
import purple from '../Assets/purple.png';


export const Homes = (courses) => {

  return (
    <>
    <div className='teacherp '>
        <div className='great user-container'><h1>Welcome back!</h1>
         <p>
        Your commitment to education is truly commendable.
        Your influence extends far beyond the classroom,<br></br>
        shaping the minds of future leaders and innovators.
        </p>
        </div>
        <div className='create-course'>
            <button>Create Course <FiUpload/></button>
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
                creation_date={course.creation_date}
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



    /*const lectures = null;
    const [lecture, setLecture] = useState(lectures);
    const [videoValid, setVideoValid] = useState(true);

    const handleChange = (e) =>{
        const video = e.target.files[0];
        if(video){
            if(video.type.startsWith('video/')){
                setLecture(video.value);
                setVideoValid(true);
            }else{
                setVideoValid(false);
            }
        }
    }

    const handleSubmit = async (e) => {
        e.preventDefault();
    }
    
    <form onSubmit={handleSubmit} className='U-container'>
       <div className='center upload'>
        <span>Lecture Video</span>
        <label htmlFor="lecture" className={!videoValid ? 'invalid' :''}>Choose Lecture 
        <span><FiUpload /></span>
        </label>
            <input type="file" id="lecture" accept="video/*" name="lecture" value={lecture} onChange={handleChange} required/>
            </div>
            {!videoValid && <div style={{ color: 'red' }}>Invalid file type. Please select a Video.</div>}

            <button type='submit'>Upload</button>
        
       </form>  */
