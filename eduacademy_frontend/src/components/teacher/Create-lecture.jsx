import React, { useState } from 'react'
import { FiUpload } from "react-icons/fi";

export const Createlecture = () => {
    const createLecture = {
        lecture_title:'',
    }

    const [form, setForm] = useState(createLecture);
    const [videoValid, setVideoValid] = useState(true);
    const [video, setvideo] = useState(null);


    const handleChange = (e) => {
        if(e.target.type==="file"){
            const file = e.target.files[0];
            if (file) {
                if (file.type.startsWith('video/')) {
                    setvideo(file)
                    setVideoValid(true);
                } else {
                    setVideoValid(false);
                    setvideo(null)
                }
        }
    }
        else{
            setForm({ ...form, [e.target.name]: e.target.value });
        }
    }

    const handleSubmit = async (e) => {
        e.preventDefault();
        Object.assign(createLecture, {'video': video})

    }
  return (
    <div className="container">
      <form onSubmit={handleSubmit} className="auth-container create_course">
        <div className='header'>
            <p className='texts'>CREATE LECTURE</p>
            <div className="underline"></div>
        </div>

        <div className="input-box">
            <input 
            type='text'
            name='lecture_title'
            id='lecture_title'
            placeholder='Lecture Title'
            value={form.lecture_title}
            onChange={handleChange}
            required
            />
        </div>

        <div className='upload package_size'>
            <span id='left'>Lecture Video</span>
            <label htmlFor="video" className={!videoValid ? 'invalid' :''}>upload Video 
            <span><FiUpload /></span>
            </label>
            <input type="file" id="video" accept="video/*"
                name="video" onChange={handleChange} required/>
        </div>
        {!videoValid && <div style={{ color: 'red' }}>Invalid file type. Please select a video.</div>}

        <div className="submit">
            <button>Create</button>
        </div>

      </form>

    </div>
  )
}
