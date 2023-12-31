import React from 'react'
import {useEffect, useState} from 'react';
import { useLocation } from 'react-router-dom';
import axios from 'axios';

const Profile = () => {

  const location = useLocation();
  const searchParams = new URLSearchParams(location.search);
  const roleParamter = searchParams.get('role');
  const usernameParamter = searchParams.get('username');
  


  const userdata = {
    view_self : true,
    username : "",
    first_name : "",
    last_name : "",
    governorate : "",
    email : "",
    date_joined : "" ,
    gender : "",
    phone_number : "",
    birth_date : "",
    user_role : "",
    academic_year : "",
    study_field : "",
    parent_phone_number : "",
    parent_name : "",
    points : "",
    balance: "",
    verified : "",
    personal_photo : null ,
    badges : "",
    national_id : ""
  };

  const [user_data, setUserData] = useState(userdata);


  useEffect(() => {
    const fetchData = async () => {
        try {
            const response = await axios.get(`/api/view_profile/${usernameParamter}`);
            setUserData(response.data);
        } catch (error) {
          console.error('Error fetching data:', error);
        }  
    };
    fetchData();
  }, []);

  return (
    <div className="profile-container">
      <div className='info'>
      <div className="profile-picture">
          <img src={user_data.personal_photo} alt="Personal Photo" />
        </div>   
        <div className="profile-details">      
        <p><span className='strong'>User Name </span> {user_data.username}</p>
        <p><span className='strong'>Name </span> {user_data.first_name + " " + user_data.last_name}</p>
        <p><span className='strong'>Governerate </span> {user_data.governorate}</p>
        <p><span className='strong'>Gender </span> {user_data.gender==='F' ? 'Female' : 'Male'}</p>
        {user_data.view_self ?(<>
          <p><span className='strong'>Email </span> {user_data.email}</p>
          <p><span className='strong'>phone number </span> 0{user_data.phone_number}</p>
        </>):
        <></>}
        <p><span className='strong'>Birth Date </span> {user_data.birth_date}</p>
        <p><span className='strong'>Date joined </span> : {user_data.date_joined}</p>
        {user_data.user_role === "Student" ?(
        <>
          <p><span className='strong'>Academic Year </span> {user_data.academic_year}</p>
          {userdata.academic_year > 10 &&    
           <p><span className='strong'>Study Field </span> {user_data.study_field}</p>
          }
          {user_data.view_self ?<>
            <p><span className='strong'>Parent Name</span> {user_data.parent_name}</p>
            <p><span className='strong'>Parent Phone Number</span> 0{user_data.parent_phone_number}</p>
            <p><span className='strong'>Points </span> {user_data.points}</p>
            <p><span className='strong'>Balance </span> {user_data.balance}</p>
            </>:
            <></>
          }
        </>
        ):<></>
        }
        { (user_data.user_role !== "Student" && user_data.view_self) ?
        (
          <p><span className='strong'>National ID </span> {user_data.national_id}</p>
        ):<></>
        }
        </div>

      </div>

    </div>
  )
}

export default Profile