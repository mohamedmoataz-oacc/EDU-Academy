import React, { useState } from 'react'
import { FiUpload } from "react-icons/fi";
import axios from 'axios';

const Createcourse = () => {
    const createCourse = {
        subject : '',
        course_name : '',
        description : '',
        lecture_price : '',
        package_size : '',
    }

    const [form, setForm] = useState(createCourse);
    const [thumbnailValid, setThumbnailValid] = useState(true);
    const [thumbnail, setThumbnail] = useState();


    const handleChange = (e) => {
        if(e.target.type==="file"){
            const file = e.target.files[0];
            if (file) {
                if (file.type.startsWith('image/')) {
                    setThumbnail(file)
                    setThumbnailValid(true);
            } else {
                setThumbnailValid(false);
                setThumbnail(null)
                
                createCourse.thumbnail=null;
            }
        }
    }
        else{
            setForm({ ...form, [e.target.name]: e.target.value });
        }
    }

    const handleSubmit = async (e) => {
        e.preventDefault();
        let response;
        const formData = new FormData();
        const csrfToken = document.cookie
        .split('; ')
        .find((row) => row.startsWith('csrftoken='))
        .split('=')[1];


        // Append form data to the FormData object
        formData.append('subject', form.subject);
        formData.append('course_name', form.course_name);
        formData.append('description', form.description);
        formData.append('lecture_price', form.lecture_price);
        formData.append('package_size', form.package_size);
        formData.append('thumbnail', thumbnail);

        try {
            response = await axios.post('/api/create_course/', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                    'X-CSRFToken': csrfToken
                },
            });

            if (response.status === 200) {
                let resp_json = response.data
                alert('Messgae: ' + resp_json.detail);
            }


        } catch (error) {
            alert('there is a proplem try again correctly')
        }
    
    }

  return (
    <div className="container">
        <form onSubmit={handleSubmit} className="auth-container create_course">
            <div className='header'>
                <p className='texts'>CREATE COURSE</p>
                <div className="underline"></div>
            </div>

            <div className="input-box">
            <label htmlFor="course_name"></label>
                <input 
                type='text'
                name='course_name'
                id='course_name'
                placeholder='Course Name'
                value={form.course_name}
                onChange={handleChange}
                required
                />
            </div>

            <div className="input-box">
                <label htmlFor="subject"></label>
                <input 
                type='text'
                name='subject'
                id='subject'
                placeholder='Subject'
                value={form.subject}
                onChange={handleChange}
                required
                />
            </div>

            <div className="input-box">
                <input 
                type='text'
                name='description'
                id='description'
                placeholder='Course Description'
                value={form.description}
                onChange={handleChange}
                required
                />
            </div>

            <div className="input-box">
                <input 
                type='text'
                name='lecture_price'
                id='lecture_price'
                placeholder='Lecture Price'
                value={form.lecture_price}
                onChange={handleChange}
                required
                />
            </div>

            <div className='package_size'>
            <label htmlFor="package_size" className=''> Package Size</label>
                <input 
                type='number'
                name='package_size'
                id='package_size'
                min='1'
                max='50'
                value={form.package_size}
                onChange={handleChange}
                required
                />
            </div>

            <div className='upload package_size'>
                <span id='left'>Course image</span>
                <label htmlFor="thumbnail" className={!thumbnailValid ? 'invalid' :''}>upload image 
                <span><FiUpload /></span>
                </label>
                <input type="file" id="thumbnail" accept="image/*"
                 name="thumbnail" value={form.thumbnail} onChange={handleChange} required/>
            </div>
            {!thumbnailValid && <div style={{ color: 'red' }}>Invalid file type. Please select an image.</div>}

            <div className="submit">
                <button>Create</button>
            </div>

        </form>
    </div>
  )
}


export default Createcourse