import React from 'react'
import useEffect from 'react';
import { useLocation } from 'react-router-dom';
import axios from 'axios';

const Profile = () => {

  const location = useLocation();
  const searchParams = new URLSearchParams(location.search);
  const roleParamter = searchParams.get('role');
  const usernameParamter = searchParams.get('username');


  const user_data = {
    view_self : true,
    username : "",
    firstname : "",
    lastname : "",
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

  user_data.username = usernameParamter ; 
  user_data.user_role = roleParamter ; 


    const fetchData = async () => {
        try {
            const response = await axios.get(`/api/view_profile/${usernameParamter}`);
            
                let reps_json = response.data ; 
                user_data.academic_year = reps_json.academic_year ; 
                user_data.badges = reps_json.badges;  
                user_data.balance = reps_json.balance ; 
                 
                user_data.date_joined = reps_json.date_joined ; 
                user_data.governorate = reps_json.governorate ; 
                user_data.verified = reps_json.verified ; 
                user_data.points = reps_json.points ; 

                user_data.email = reps_json.email ; 
                user_data.gender = reps_json.gender ;
                user_data.birth_date = reps_json.birth_date;

                user_data.firstname = reps_json.first_name ;
                user_data.lastname = reps_json.last_name ;
                user_data.parent_name = reps_json.parent_name ;
                user_data.parent_phone_number = reps_json.parent_phone_number ; 
                user_data.phone_number  = reps_json.phone_number ;
                
              console.log(11111111111111)


        } catch (error) {

            
        }
    };

    fetchData();





  return (
    <div className="profile-container">
      <div className='info'>
      <div className="profile-picture">
          <img src={user_data.personal_photo} alt="Personal Photo" />
        </div>        
        <p><span className='strong'>User Name </span> {user_data.username}</p>
        <p><span className='strong'>Name </span> {user_data.firstname + " " + user_data.lastname}</p>
        <p><span className='strong'>Governerate </span> {user_data.governorate}</p>
        <p><span className='strong'>Gender </span> {user_data.gender}</p>
        {user_data.view_self ?(<>
          <p><span className='strong'>Email </span> {user_data.email}</p>
          <p><span className='strong'>phone number </span> {user_data.phone_number}</p>
        </>):
        <></>}
        <p><span className='strong'>Birth Date </span> {user_data.birth_date}</p>
        <p><span className='strong'>Date joined </span> : {user_data.date_joined}</p>
        {user_data.user_role === "Student" ?(
        <>
          <p><span className='strong'>Academic Year </span> {user_data.academic_year}</p>
          <p><span className='strong'>Study Field </span> {user_data.study_field}</p>
          {user_data.view_self ?<>
            <p><span className='strong'>Parent Name</span> {user_data.parent_name}</p>
            <p><span className='strong'>Parent Phone Number</span> {user_data.parent_phone_number}</p>
            <p><span className='strong'>Points </span> {user_data.points}</p>
            <p><span className='strong'>Balance </span> {user_data.balance}</p>
            </>:
            <></>
          }
          <p><span className='strong'>User Name </span> {user_data.username}</p>
        </>
        ):<></>
        }
        { (user_data.user_role !== "Student" && user_data.view_self) ?
        (
          <p><span className='strong'>National ID </span> {user_data.national_id}</p>
        ):<></>
        }
        {
          user_data.user_role !== "Teacher" ?
          <p><span className='strong'>Balance </span> {user_data.balance}</p>

          :<></>
        }

      </div>

      <div></div>
      <div></div>
    </div>
  )
}

export default Profile