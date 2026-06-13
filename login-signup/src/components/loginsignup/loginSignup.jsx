import React, { useState } from 'react'
import './loginSignup.css'
import user_icon from '../../assets/user_icon.png'
import email_icon from '../../assets/email_icon.png'
import password_icon from '../../assets/password_icon.png'

export const LoginSignup = () => {
  const [action, setAction] = useState('signup')

  return (
    <div className="container">
      <div className="header">
        <div className="text">{action === 'signup' ? 'Sign Up' : 'Login'}</div>
        <div className="underline"></div>
      </div>

      <form className="inputs" onSubmit={(e) => e.preventDefault()}>
        {action === 'signup' && (
          <div className="input">
            <img src={user_icon} alt="User Icon" />
            <input type="text" placeholder="Username" />
          </div>
        )}

        <div className="input">
          <img src={email_icon} alt="Email Icon" />
          <input type="email" placeholder="Email" />
        </div>

        <div className="input">
          <img src={password_icon} alt="Password Icon" />
          <input type="password" placeholder="Password" />
        </div>
      </form>

      {action === 'login' && (
        <div className="forgot-password">
          <button type="button" onClick={() => {}}>Forgot Password?</button>
        </div>
      )}

      <div className="submit-container">
        <button
          type="button"
          className={`submit ${action === 'signup' ? '' : 'gray'}`}
          onClick={() => setAction('signup')}
        >
          Sign Up
        </button>
        <button
          type="button"
          className={`submit ${action === 'login' ? '' : 'gray'}`}
          onClick={() => setAction('login')}
        >
          Login
        </button>
      </div>
    </div>
  )
}

export default LoginSignup
 