import React from 'react'

export const Profile = () => {
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
  return (
    <div>
      <div className='info'>
        <p><span className='strong'>Personal Photo </span> <img src={user_data.personal_photo} alt="personal photo" /></p>
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
