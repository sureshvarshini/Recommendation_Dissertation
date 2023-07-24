// This file will hold all the navigation bar components which will be in link format
import React from 'react'
import { Link } from 'react-router-dom'
import { useAuth, logout } from '../Auth'
import logo from "../assets/Assist_wise_logo.png"
import avatar from "../assets/avatar.jpg"

// The links/buttons that are available to a logged in user.
const LoggedInLinks = () => {
  return (
    <>
      <li className="nav-item">
        <Link className="nav-link active" to="/">Home</Link>
      </li>
      <li className="nav-item">
        <a className="nav-link active" href='/' onClick={() => { logout() }}>Logout</a>
      </li>
      <li className="nav-item">
        <Link className="nav-link active" to="/myaccount">My Account</Link>
      </li>
    </>
  )
}

// The links/buttons that are available to a logged out user/new user who wants to sign up.
const LoggedOutLinks = () => {
  return (
    <>
      <li className="nav-item">
        <Link className="nav-link active" to="/">Home</Link>
      </li>
      <li className="nav-item">
        <Link className="nav-link active" to="/login">Login</Link>
      </li>
    </>
  )
}

const Navbar = () => {

  const [isUserLoggedIn] = useAuth()

  return (
    <nav className="navbar navbar-expand-lg navbar-dark bg-dark fixed-top">
      <div className="container-fluid">
        <a style={{ fontSize: '20px' }} className="navbar-brand" href="/">
          <img src={logo} class="me-2" height="40" loading="lazy" />
          AssistWise
        </a>
        <div className="rightside" id="navbarNav">
          <ul className="navbar-nav">{isUserLoggedIn ? <LoggedInLinks /> : <LoggedOutLinks />}</ul>
        </div>
      </div>
    </nav>
  )
}

export default Navbar
