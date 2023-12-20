import React, { useEffect, useState } from 'react';
import { FiUpload } from "react-icons/fi";
import { useLocation } from 'react-router-dom';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';



const CompleteProfile = () => {


    const navigate = useNavigate();
    const location = useLocation();
    const searchParams = new URLSearchParams(location.search);
    const role = searchParams.get('role');



    // ensure the user is authnticated
    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await axios.get('/api/complete_profile/', { maxRedirects: 0 });
            } catch (error) {
                if (error.response.status === 403) {
                    alert(`Message: ${error.response.data}`)
                    navigate({
                        pathname: '/Login'
                    });
                }
            }
        };

        fetchData();
    }, [navigate]);




    const complete_profile = {
        personal_photo: null,
        National_ID_photo: null,
        academic_year: null,
        study_field: null,
        parent_name: "",
        parent_phone_number: "",
    }
    const study_field = ['أدبي', 'علمي علوم', 'علمي رياضة']
    const study_field2 = ['أدبي', 'علمي']

    const [form, setForm] = useState(complete_profile);
    const [personalValid, setPersonalValid] = useState(true);
    const [nationalValid, setNationalValid] = useState(true);


    const handleChange = (e) => {
        if (e.target.type === "file" && e.target.name === 'personal_photo') {
            const file = e.target.files[0];
            if (file) {
                if (file.type.startsWith('image/')) {
                    setForm({ ...form, [e.target.name]: file });
                    setPersonalValid(true);
                } else {
                    setPersonalValid(false);
                }
            }
        } else if (e.target.type === "file" && e.target.name === 'National_ID_photo') {
            const file = e.target.files[0];
            if (file) {
                if (file.type.startsWith('image/')) {
                    setForm({ ...form, [e.target.name]: file });
                    setNationalValid(true);
                } else {
                    setNationalValid(false);
                }
            }
        } else {
            setForm({ ...form, [e.target.name]: e.target.value });
        }
    }

    const handleSubmit = async (e) => {
        e.preventDefault();

        const formData = new FormData();
        const csrfToken = document.cookie
            .split('; ')
            .find((row) => row.startsWith('csrftoken='))
            .split('=')[1];


        let response;
        formData.append('personal_photo', form.personal_photo);
        if (role === 'Student') {

            formData.append('academic_year', form.academic_year);
            formData.append('parent_name', form.parent_name);
            formData.append('parent_phone_number', form.parent_phone_number);
            if (form.study_field !== null) {
                formData.append('study_field', form.study_field);
            }

        } else {
            formData.append('National_ID_photo', form.National_ID_photo);
        }


        try {
            response = await axios.post('/api/complete_profile/', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                    'X-CSRFToken': csrfToken
                },
            });

            if (response.status === 200) {
                let resp_json = response.data
                alert('Messgae: ' + resp_json.detail);
                navigate({
                    pathname: `${resp_json.redirect_to}`,
                    search: `?role=${resp_json.user_role}&username=${resp_json.username}`, // Pass user_role as a query parameter
                });
            }


        } catch (error) {
            alert('there is a proplem try again correctly')
        }

    }


    return (
        <div className="container">

            <form className='complete-profile' onSubmit={handleSubmit}>
                <div className='header'>
                    <p className='texts'>Complete Profile</p>
                    <div className="underline"></div>
                </div>
                {role === 'Student' ? (
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
                                : <></>
                        }
                        {
                            form.academic_year === '11' ?
                                <div className='center'>
                                    <label for="study_field">Academic Year: </label>
                                    <select
                                        name='study_field'
                                        id="study_field"
                                        value={form.study_field}
                                        onChange={handleChange}
                                    >
                                        {study_field2.map((field, index) => (
                                            <option key={index + 1} value={index + 1}>
                                                {field}
                                            </option>
                                        ))}

                                    </select>

                                </div>
                                : <></>
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
                ) :
                    <></>

                }
                <div class='center upload'>
                    <span>Personal photo</span>
                    <label for="personal" class={!personalValid ? 'invalid' : ''}>
                        Upload photo
                        <span><FiUpload /></span>
                    </label>
                    <input type="file" id="personal" accept="image/*" name="personal_photo" onChange={handleChange} required />
                    {!personalValid && <div style="color: red;">Invalid file type. Please select an image.</div>}
                </div>

                {role !== 'Student' ? (
                    <div class='center upload'>
                        <span>NationalID photo</span>
                        <label for="national" class={!nationalValid ? 'invalid' : ''}>
                            Upload photo
                            <span><FiUpload /></span>
                        </label>
                        <input type="file" id="national" accept="image/*" name="National_ID_photo" onChange={handleChange} required />
                        {!nationalValid && <div style="color: red;">Invalid file type. Please select an image.</div>}
                    </div>
                ) : ''}
                <div className="submit">
                    {/* 
                we will skip this skip for now
                <button type='button'>Skip</button> 
                */}

                    <button type='submit'>Submit</button>
                </div>

            </form>
        </div>
    )
}

export default CompleteProfile