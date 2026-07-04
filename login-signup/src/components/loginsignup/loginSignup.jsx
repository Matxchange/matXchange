import React, { useState } from 'react'
import { Link } from 'react-router-dom'
import './loginSignup.css'
import mx_logo from '../assets/mx-logo.png'

const UserIcon = () => (
  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
    <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
    <circle cx="12" cy="7" r="4"/>
  </svg>
)

const EmailIcon = () => (
  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
    <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/>
    <polyline points="22,6 12,13 2,6"/>
  </svg>
)

const LockIcon = () => (
  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
    <rect x="3" y="11" width="18" height="11" rx="2" ry="2"/>
    <path d="M7 11V7a5 5 0 0 1 10 0v4"/>
  </svg>
)

const EyeIcon = () => (
  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
    <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/>
    <circle cx="12" cy="12" r="3"/>
  </svg>
)

const EyeOffIcon = () => (
  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
    <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94"/>
    <path d="M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19"/>
    <line x1="1" y1="1" x2="23" y2="23"/>
  </svg>
)


const LoginSignup = () => {
  const [action, setAction] = useState('signup')
  const [showPassword, setShowPassword] = useState(false)

  return (
    <div className="login-page">
      <div className="login-card">

        <Link to="/" className="login-back">← Back to home</Link>

        <div className="login-logo-wrap">
          <img src={mx_logo} alt="MatXchange" className="login-logo" />
        </div>

        <div className="login-header">
          <div className="login-title">{action === 'signup' ? 'Create Account' : 'Welcome Back'}</div>
          <div className="login-underline" />
        </div>

        <form className="login-inputs" onSubmit={(e) => e.preventDefault()}>
          {action === 'signup' && (
            <div className="login-input">
              <span className="input-icon"><UserIcon /></span>
              <input type="text" placeholder="Username" />
            </div>
          )}

          <div className="login-input">
            <span className="input-icon"><EmailIcon /></span>
            <input type="email" placeholder="Email" />
          </div>

          <div className="login-input">
            <span className="input-icon"><LockIcon /></span>
            <input type={showPassword ? 'text' : 'password'} placeholder="Password" />
            <button
              type="button"
              className="eye-toggle"
              onClick={() => setShowPassword(p => !p)}
              aria-label={showPassword ? 'Hide password' : 'Show password'}
            >
              {showPassword ? <EyeOffIcon /> : <EyeIcon />}
            </button>
          </div>
        </form>

        {action === 'login' && (
          <div className="login-forgot">
            <button type="button">Forgot Password?</button>
          </div>
        )}

        <div className="login-actions">
          <button
            type="button"
            className={`login-btn ${action === 'signup' ? 'active' : 'ghost'}`}
            onClick={() => setAction('signup')}
          >
            Sign Up
          </button>
          <button
            type="button"
            className={`login-btn ${action === 'login' ? 'active' : 'ghost'}`}
            onClick={() => setAction('login')}
          >
            Log In
          </button>
        </div>
      </div>
    </div>
  )
}

export default LoginSignup