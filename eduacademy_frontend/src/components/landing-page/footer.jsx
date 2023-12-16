import React from 'react'
import { IoMdHome } from "react-icons/io";
import { HiOutlineMail } from "react-icons/hi";
import { FiPhone } from "react-icons/fi";
import { BiLogoFacebookCircle } from "react-icons/bi";



export const Footer = () => {
  return (
    <div className='footer' id="footer">
        <div className='col1'>
            <h6>Contact</h6>
            <div><span><HiOutlineMail /></span><p> info@gmail.com</p></div>
            <div><span><FiPhone /></span><p>+20 1234 567 889</p></div>
            
        </div>
    </div>
  )
}
