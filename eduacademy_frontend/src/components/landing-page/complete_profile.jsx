import React from 'react'
import { FiUpload } from "react-icons/fi";

import { useState} from 'react';


export const Completeprofile = (role) => {

    const complete_profile={
        personal_photo:null,
        National_ID_photo: null,
        academic_year: null,
        study_field: null,
        parent_name: "",
        parent_phone_number:"",
    }
    const study_field = ['أدبي' , 'علمي علوم' ,'علمي رياضة']
    const study_field2 = ['علمي','أدبي']

  const [form, setForm] = useState(complete_profile);
  const [personalValid, setPersonalValid] = useState(true);
  const [nationalValid, setNationalValid] = useState(true);


  const handleChange = (e) => {
    if(e.target.type==="file" && e.target.name === 'personal_photo'){
        const file = e.target.files[0];
        if (file) {
            if (file.type.startsWith('image/')) {
                setForm({ ...form, [e.target.name]: e.target.value });
                console.log(e.target.value)
                setPersonalValid(true);
        } else {
            setPersonalValid(false);
        }
      }
    }else if(e.target.type==="file" && e.target.name === 'National_ID_photo'){
        const file = e.target.files[0];
        if (file) {
            if (file.type.startsWith('image/')) {
                setForm({ ...form, [e.target.name]: e.target.value });
                console.log(e.target.value)
                setNationalValid(true);
        } else {
            setNationalValid(false);
        }
    }
}
    else{
        setForm({ ...form, [e.target.name]: e.target.value });
        console.log(e.target.value)
    }
    console.log(form)
 }

  return (
    <div className="container">
        
    <form className='complete-profile'>
        <div className='header'>
            <p className='texts'>Complete Profile</p>
            <div className="underline"></div>
        </div>
        {role === 'Student' ?(
            <>
                <div className='center'>
                    <label for="academic_year">Academic Year </label>
                    <select
                        name='academic_year'
                        id="academic_year"
                        value={form.academic_year}
                        onChange={handleChange}
                    >
                        {[...Array(12).keys()].map((number) => (
                        <option key={number + 1} value={number + 1}>
                            {number + 1}
                        </option>
                        ))}
                    </select> 

                </div>
                {
                    form.academic_year === '12' ?
                    <div className='center'>
                    <label for="study_field">Study Field </label>
                    <select
                        name='study_field'
                        id="study_field"
                        value={form.study_field}
                        onChange={handleChange}
                    >
                        {study_field.map((field, index) => (
                        <option key={index} value={index}>
                            {field}
                        </option>
                        ))}
                        
                    </select> 

                </div>
                    :<></>
                }
                {
                    form.academic_year === '11' ?
                    <div className='center'>
                    <label for="study_field">Academic Year: </label>
                    <select
                        name='study_field'
                        id="study_field"
                        value={form.academic_year}
                        onChange={handleChange}
                    >
                        {study_field2.map((field, index) => (
                        <option key={index} value={index}>
                            {field}
                        </option>
                        ))}
                        
                    </select> 

                </div>
                    :<></>
                }
                <div className='center'>
                    <label htmlFor="parent_name">Parent Name </label>
                    <input id="parent_name" 
                    type='text'
                    value={form.parent_name}
                    name="parent_name"
                    onChange={handleChange} />
                </div>
                <div className='center'>
                    <label htmlFor="parent_phone_number">Parent Phone Number </label>
                    <input id="parent_phone_number"
                     type='text'
                     value={form.parent_phone_number}
                     name="parent_phone_number"
                      onChange={handleChange} />
                </div>
            </>
        ):
        <></>

        }
        <div className='center upload'>
            <span>Personal photo</span>
            <label htmlFor="personal" className={!personalValid ? 'invalid' :''}>upload photo
            <span><FiUpload /></span>
            </label>
            <input type="file" id="personal" accept="image/*" name="personal_photo" value={form.personal_photo} onChange={handleChange} required/>
            {!personalValid && <div style={{ color: 'red' }}>Invalid file type. Please select an image.</div>}
        </div>
        {role !== 'Student' ?(
            <div className='center upload'>
            <span>NationalID photo</span>
            <label htmlFor="national" className={!nationalValid ? 'invalid' :''}>upload photo 
            <span><FiUpload /></span>
            </label>
                <input type="file" id="national" accept="image/*" name="National_ID_photo" value={form.personal_photo} onChange={handleChange} required/>
                {!nationalValid && <div style={{ color: 'red' }}>Invalid file type. Please select an image.</div>}
            </div>
        ):<></>
        }
        <div className="submit">
            <button>Skip</button>
            <button>Submit</button>
            
        </div>

    </form>
    </div>
  )
}

