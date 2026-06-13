import React from 'react'
import './loginSignup.css'
import user_icon from '../../assets/mx-logo.png'
import email_icon from '../../assets/mx-logo.png'
import password_icon from '../../assets/mx-logo.png'

export const loginSignup = () => {
  return (
    <div className="container" >
      <div className="header">
        <div className="text">Sign Up</div>
        <div className="underline"></div>
      </div>

      <div className="inputs"></div>
      <div className="input">
        <img src="" alt="" />
        <input type="text"/>
      </div>

      <div className="input">
        <img src="" alt="" />
        <input type="email"/>
      </div>

      <div className="input">
        <img src="" alt="" />
        <input type="password"/>
      </div>
    </div>
  )
}

export default loginSignup
 