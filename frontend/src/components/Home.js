import React from 'react'
import { Link } from 'react-router-dom'
import { useAuth } from '../Auth'

// View contents based on whether a user is logged in or a new user
// Need to add recommendations end point related content
const LoggedInHomePage = () => {
    return (
        <div className="Recommendation container">
            <h1>Welcome back to AssistWise</h1>
            <h4>View your food recommendations <Link to='/recommendations/food'>here</Link> </h4>
            <br></br>
            <h4>View your water tracker <Link to='/recommendations/water'>here</Link></h4>
        </div>
    )
}

const NewUserHomePage = () => {
    return (
        <div className="Home container">
            <h1>Welcome to AssistWise</h1>
            <h3>Let's begin your personalized recommendations journey. The first step is just a click away.</h3>
            <Link to='/signup' className="btn btn-primary">Get started now.</Link>
        </div>
    )
}

const HomePage = () => {
    const [isUserLoggedIn] = useAuth()
    return (
        <div>
            {isUserLoggedIn ? <LoggedInHomePage /> : <NewUserHomePage />}
        </div>
    )
}

export default HomePage