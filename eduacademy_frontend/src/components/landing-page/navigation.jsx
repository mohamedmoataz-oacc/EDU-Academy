import React from 'react'
import { CustomLink } from './customlink'


export const Navigation = () => {

  return (
    <div className='nav'>
      <CustomLink className="About Link" to="">About</CustomLink>
      <CustomLink className="teacher Link" to="/teacher">Teachers</CustomLink>
      <a className="contact Link" href='/#footer'>Contact</a>
      <CustomLink className="login" to="/login">Login</CustomLink>
    </div>

  )
}


