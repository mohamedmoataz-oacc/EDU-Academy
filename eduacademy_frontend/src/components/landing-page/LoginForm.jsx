import React, { useState } from 'react';
import facebook from '../Assets/facebook.png'
import google from '../Assets/google.png'


const initialState = {
    fName: '',
    lName: '',
    username: '',
    password: '',
    confirmPassword: '',
    phoneNumber: '',
    avatarURL: '',
}



const Auth = () => {
    const [form, setForm] = useState(initialState);
    const [isSignup, setIsSignup] = useState(true);

    const handleChange = (e) => {
        setForm({ ...form, [e.target.name]: e.target.value });
    }

    const handleSubmit = async (e) => {
        e.preventDefault();
        window.location.reload();
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
                            <span><img src={google} alt="google" height="30px" width="30px"/></span>
                            {isSignup
                             ? "Sign up with Google" 
                             : "Sign in with Google "
                             }
                        </button>
                        <button>
                            <span><img src={facebook} alt="facebook" height="30px" width="30px"/></span>
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
                        {isSignup && (

                            <div className="input-box name" id='name'>
                                <div className="lfname">
                                <input 
                                    name="fName" 
                                    type="text"
                                    placeholder='First Name'
                                    onChange={handleChange}
                                    required
                                />
                                </div>
                                <div className="lfname">
                                <input 
                                    name="lName" 
                                    type="text"
                                    placeholder='Last Name'
                                    onChange={handleChange}
                                    required
                                />
                                </div>
                            </div>
                        )}
                        <div className="input-box">
                                <input 
                                    name="email" 
                                    type="email"
                                    placeholder='Email'
                                    onChange={handleChange}
                                    required
                                />
                            </div>
                        {isSignup && (
                            <div className="input-box">
                                <input 
                                    name="phoneNumber" 
                                    type="text"
                                    placeholder="Phone Number"
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
                                    onChange={handleChange}
                                    required
                                />
                            </div>
                            )}
                            {isSignup && (
                            <div className="role">
                                <input type="radio" id='student' value="Student" name="role"/>
                                <label for="student" >Student</label>
                                <input type="radio" id='teacher' value="Teacher" name="role" />
                                <label for="teacher" >Teacher</label>
                                <input type="radio" id='assistant' value="assistant" name="role" />
                                <label for="assistant" >Assistant</label>
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