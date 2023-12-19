import React, { useEffect, useState } from 'react';
import facebook from '../Assets/facebook.png'
import google from '../Assets/google.png'
import axios from 'axios';
import { useNavigate } from 'react-router-dom';


const initialState = {
    username: '',
    first_name: '',
    last_name: '',
    email: '',
    password: '',
    confirmPassword: '',
    phone_number: '',
    governorate: '',
    gender: '',
    user_role: 2,
    birth_date: ''
}


const governorates = [
    'Cairo',
    'Alexandria',
    'Ismailia',
    'Kafr El Sheikh',
    'Port Said',
    'Suez',
    'Dakahlia',
    'Damietta',
    'Faiyum',
    'Gharbia',
    'Luxor',
    'Matrouh',
    'Minya',
    'Monufia',
    'New Valley',
    'North Sinai',
    'Qalyubia',
    'Qena',
    'Red Sea',
    'Sharqia',
    'Sohag',
    'Aswan',
    'Asyut',
    'Beni Suef',
    'Beheira',
    'Helwan',
];




const Auth = () => {
    const navigate = useNavigate();
    const [form, setForm] = useState(initialState);
    const [isSignup, setIsSignup] = useState(true);

    const handleChange = (e) => {
        setForm({ ...form, [e.target.name]: e.target.value });
    }

    const handleSubmit = async (e) => {
        e.preventDefault();
        let response;


        if (isSignup) {
            // If it's a signup operation, send a request to the signup API
            try {
                response = await axios.post('/api/signup/', {
                    username: form.username,
                    email: form.email,
                    password: form.password,
                    confirmPassword: form.confirmPassword,
                    first_name: form.first_name,
                    last_name: form.last_name,
                    governorate: form.governorate,
                    phone_number: Number(form.phone_number),
                    gender: form.gender,
                    user_role: form.user_role,
                    birth_date: form.birth_date

                }, { maxRedirects: 0 })


                if (response.status === 200) {
                    alert('Message:' + response.data);
                    setIsSignup(false)
                }


            } catch (error) {
                if (error.response.status === 400) {
                    alert(`Message: Your information is badly formatted OR there is user with the same username OR email address PLease try again`)
                } else if (error.response.status === 403) {
                    alert('Message: You Already Loged In');
                } else {
                    alert('Message: Unkown/Netwrok error');
                }
            }


        } else {
            // If it's a login operation, send a request to the login API
            try {
                response = await axios.post('/api/login/', {
                    username: form.username,
                    password: form.password,
                },);


                if (response.status === 200) {
                    alert('Message: Logged in successfully');
                    let resp_json = response.data;
                    // debug
                    // console.log('role:', resp_json.user_role);
                    // console.log('url:', resp_json.redirect_to);

                    if (resp_json.redirect_to === undefined) {
                        navigate({
                            pathname: `/Home`
                        });
                    } else {
                        navigate({
                            pathname: `${resp_json.redirect_to}`,
                            search: `?role=${resp_json.user_role}`, // Pass user_role as a query parameter
                        });
                    }
                }

            } catch (error) {
                if (error.response.status === 404) {
                    alert('Message:' + error.response.data);
                } else if (error.response.status === 403) {
                    alert('Message: You Already Loged In');
                } else {
                    alert('Message: Unkown/Netwrok error');
                }
            }

        }




    }

    const switchMode = () => {
        setIsSignup((prevIsSignup) => !prevIsSignup);
    }

    return (
        <div className="container">
            <div className="auth-container">
                <div className='header'>
                    <p className='texts'>{isSignup ? 'SIGN UP' : 'SIGN IN'}</p>
                    <div className="underline"></div>
                </div>
                <div className='social-media' >
                    <button>
                        <span><img src={google} alt="google" height="30px" width="30px" /></span>
                        {isSignup
                            ? "Sign up with Google"
                            : "Sign in with Google "
                        }
                    </button>
                    <button>
                        <span><img src={facebook} alt="facebook" height="30px" width="30px" /></span>
                        {isSignup
                            ? "Sign up with Facebook"
                            : "Sign in with Facebook"
                        }
                    </button>
                </div>
                <div className='or'>
                    <div className='line'></div>
                    <span>
                        or
                    </span>
                    <div className='line'></div>

                </div>
                <form className='inputs' onSubmit={handleSubmit}>
                    {
                        <div className="input-box">
                            <input
                                name="username"
                                type="text"
                                placeholder="User Name"
                                value={form.username}
                                onChange={handleChange}
                                required
                            />
                        </div>
                    }

                    {isSignup && (
                        <>
                            <div className="input-box name" id='name'>
                                <div className="lfname">
                                    <input
                                        name="first_name"
                                        type="text"
                                        placeholder='First Name'
                                        value={form.first_name}
                                        onChange={handleChange}
                                        required
                                    />
                                </div>
                                <div className="lfname">
                                    <input
                                        name="last_name"
                                        type="text"
                                        placeholder='Last Name'
                                        value={form.last_name}
                                        onChange={handleChange}
                                        required
                                    />
                                </div>
                            </div>
                            <div className="input-box">
                                <input
                                    name="email"
                                    type="email"
                                    placeholder='Email'
                                    value={form.email}
                                    onChange={handleChange}
                                    required
                                />
                            </div>
                        </>
                    )}



                    {isSignup && (
                        <div className="input-box">
                            <input
                                name="phone_number"
                                type="tel"
                                pattern="[0-9]{10}"
                                placeholder="Phone Number"
                                value={form.phone_number}
                                onChange={handleChange}
                                required
                            />
                        </div>
                    )}
                    <div className="input-box">
                        <input
                            name="password"
                            type="password"
                            placeholder='Password'
                            value={form.password}
                            onChange={handleChange}
                            required
                        />
                    </div>
                    {isSignup && (
                        <div className="input-box">
                            <input
                                name="confirmPassword"
                                type="password"
                                placeholder='confirmPassword'
                                value={form.confirmPassword}
                                onChange={handleChange}
                                required
                            />
                        </div>
                    )}
                    {isSignup && (
                        <div>
                            <label for="governorateSelect">Select Governorate: </label>
                            <select
                                name='governorate'
                                id="governorateSelect"
                                value={form.governorate}
                                onChange={handleChange}
                            >
                                <option value="">Select...</option>
                                {governorates.map((governorate) => (
                                    <option key={governorate} value={governorate}>
                                        {governorate}
                                    </option>
                                ))}
                            </select>

                        </div>
                    )}

                    {isSignup && (
                        <div className="gender">
                            Gender:
                            <input type="radio"
                                id='Male'
                                value="M"
                                name="gender"
                                onChange={handleChange}
                                checked={form.gender === 'M'}
                            />
                            <label for="Male" >Male</label>
                            <input type="radio"
                                id='Female'
                                value="F"
                                name="gender"
                                checked={form.gender === 'F'}
                                onChange={handleChange} />
                            <label for="Female" >Female</label>

                        </div>
                    )}
                    {isSignup && (
                        <div className="role">
                            <input
                                type="radio"
                                id="student"
                                value='Student'
                                name="user_role"
                                checked={form.user_role === 'Student'}
                                onChange={handleChange}
                            />
                            <label htmlFor="student">Student</label>

                            <input
                                type="radio"
                                id="teacher"
                                value='Teacher'
                                name="user_role"
                                checked={form.user_role === 'Teacher'}
                                onChange={handleChange}
                            />
                            <label htmlFor="teacher">Teacher</label>

                            <input
                                type="radio"
                                id="assistant"
                                value='Assistant'
                                name="user_role"
                                checked={form.user_role === 'Assistant'}
                                onChange={handleChange}
                            />
                            <label htmlFor="assistant">Assistant</label>
                        </div>
                    )}
                    {isSignup && (
                        <div className="input-box">
                            <label htmlFor="birth_date">Date of Birth:</label>
                            <input
                                name="birth_date"
                                type="date"
                                value={form.dateOfBirth}
                                onChange={handleChange}
                                required
                            />
                        </div>
                    )}

                    <div className="submit">
                        <button>{isSignup ? "Sign Up" : "Sign In"}</button>
                    </div>
                </form>
                <div className="login-signup">
                    <p>
                        {isSignup
                            ? "Already have an account? "
                            : "Don't have an account? "
                        }
                        <span onClick={switchMode}>
                            {isSignup ? 'Sign In' : 'Sign Up'}
                        </span>
                    </p>
                </div>
            </div>
        </div>
    )
}

export default Auth
