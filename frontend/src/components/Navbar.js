// This file will hold all the navigation bar components which will be in link format

import React, { useState } from 'react'
import { Link } from 'react-router-dom'
import { useAuth, logout } from '../Auth'

// The links/buttons that are available to a logged in user.
const LoggedInLinks = () => {
  return (
    <>
      <li className="nav-item">
        <Link className="nav-link active" to="/">Home</Link>
      </li>
      <li className="nav-item">
        <a className="nav-link active" href='#' onClick={() => { logout() }}>Logout</a>
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
        <Link className="nav-link active" to="/signup">Sign-Up</Link>
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
    <nav className="navbar navbar-expand-lg navbar-dark bg-dark">
      <div className="container-fluid">
        <Link className="navbar-brand" to="/">AssistWise</Link>
        <button className="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
          <span className="navbar-toggler-icon"></span>
        </button>
        <div className="collapse navbar-collapse" id="navbarNav">
          <ul className="navbar-nav">
            {isUserLoggedIn ? <LoggedInLinks /> : <LoggedOutLinks />}
          </ul>
        </div>
      </div>
    </nav>
  )
}

export default Navbar
