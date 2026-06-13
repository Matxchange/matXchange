import React from 'react'
import './loginSignup.css'
import user_icon from '../../assets/user_icon.png'
import email_icon from '../../assets/mx-logo.png'
import password_icon from '../../assets/password_icon.png'

export const loginSignup = () => {
  return (
    <div className="container" >
      <div className="header">
        <div className="text">Sign Up</div>
        <div className="underline"></div>
      </div>

      <div className="inputs">
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

      <div className="forgot-password"></div>
      <div className="submit container">
        <div className="submit"> Sign up</div>
        <div className="submit"> Login</div>
      </div>
    </div>
  )
}

export default loginSignup
 