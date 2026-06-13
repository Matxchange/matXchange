import React, { useState } from 'react'
import './loginSignup.css'
import user_icon from '../assets/user_icon.png'
import email_icon from '../assets/email_icon.png'
import password_icon from '../assets/password_icon.png'

const EyeIcon = () => (
  <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none"
    stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z" />
    <circle cx="12" cy="12" r="3" />
  </svg>
)

const EyeOffIcon = () => (
  <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none"
    stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94" />
    <path d="M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19" />
    <line x1="1" y1="1" x2="23" y2="23" />
  </svg>
)

export const LoginSignup = () => {
  const [action, setAction] = useState('signup')
  const [showPassword, setShowPassword] = useState(false)

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
          <input type={showPassword ? 'text' : 'password'} placeholder="Password" />
          <button
            type="button"
            className="eye-toggle"
            onClick={() => setShowPassword(prev => !prev)}
            aria-label={showPassword ? 'Hide password' : 'Show password'}
          >
            {showPassword ? <EyeOffIcon /> : <EyeIcon />}
          </button>
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
 