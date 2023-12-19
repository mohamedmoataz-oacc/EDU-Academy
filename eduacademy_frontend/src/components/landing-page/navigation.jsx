import React from 'react'
import { CustomLink } from './customlink'


export const Navigation = () => {

  return (
    <div className='nav'>
      <CustomLink className="About Link" to="">About</CustomLink>
      <CustomLink className="teacher Link" to="/Teacher">Teachers</CustomLink>
      <a className="contact Link" href='/#footer'>Contact</a>
      <CustomLink className="login" to="/Login">Login</CustomLink>
    </div>

  )
}


