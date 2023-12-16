import React from 'react'
import { CustomLink } from '../landing-page/customlink'

export const Navbar = () => {
  return (
    <div className='nav profile'>
        <CustomLink className = "home Link" to="/">My Courses</CustomLink>
        <CustomLink className = "home Link" to="/Courses">Profile</CustomLink>
        <CustomLink className = "home Link" to="/profile">Enroll Course</CustomLink>
        <CustomLink className = "home Link" to="/profile">Settings</CustomLink>
    </div>
  )
}
