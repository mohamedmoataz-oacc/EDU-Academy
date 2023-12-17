import React, { useState } from 'react';
import facebook from '../Assets/facebook.png'
import google from '../Assets/google.png'


const initialState = {
    username: '',
    first_name: '',
    last_name: '',
    email:'',
    password: '',
    confirmPassword: '',
    phoneNumber: '',
    governerate: '',
    phone_number: '',
    gender: '',
    user_role:'',

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
                            <>
                            <div className="input-box name" id='name'>
                                <div className="lfname">
                                <input 
                                    name="fName" 
                                    type="text"
                                    placeholder='First Name'
                                    value={form.first_name}
                                    onChange={handleChange}
                                    required
                                />
                                </div>
                                <div className="lfname">
                                <input 
                                    name="lName" 
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

                        {!isSignup && (
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
                        )}
                        
                        {isSignup && (
                            <div className="input-box">
                                <input 
                                    name="phoneNumber" 
                                    type="text"
                                    placeholder="Phone Number"
                                    value={form.phoneNumber}
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
                                  name='governerate'
                                  id="governorateSelect"
                                  value={form.governerate}
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
                            <div className="role">
                                Gender:  
                                <input type="radio" id='Male' value="male" name="gender"
                                onChange={handleChange }
                                checked={form.gender === 'male' }
                                />
                                <label for="Male" >Male</label>
                                <input type="radio" id='Female' value="female" name="gender" 
                                checked={form.gender === 'female'}
                                onChange={handleChange}/>
                                <label for="Female" >Female</label>
                                
                            </div>
                            )}
                            {isSignup && (
                            <div className="role">
                                <input type="radio" id='student' value='student' name="user_role"
                                checked={form.user_role === 'student'}
                                onChange={handleChange}/>
                                <label for="student" >Student</label>
                                <input type="radio" id='teacher' value='teacher' name="user_role" 
                                checked={form.user_role === 'teacher'}
                                onChange={handleChange}/>
                                <label for="teacher" >Teacher</label>
                                <input type="radio" id='assistant' value='assistant' name="user_role" 
                                checked={form.user_role === 'assistant'}
                                onChange={handleChange}/>
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
