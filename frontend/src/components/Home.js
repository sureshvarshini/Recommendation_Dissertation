import React, { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { useAuth, login, logout } from '../Auth'
import axios from 'axios'
import homeImage from "../assets/elderly_home.jpg"
import foodBackground from "../assets/food_background.jpg"
import foodRecommendation from "../assets/food_recommendation.jpg"
import waterRecommendation from "../assets/water_recommendation.jpg"
import activity from "../assets/elderly_activity.jpg"
import home_1 from "../assets/home_1.jpg"
import home_2 from "../assets/home_2.jpg"
import home_3 from "../assets/home_3.jpg"
import home_5 from "../assets/home_5.jpg"
import home_6 from "../assets/home_6.jpg"
import home_7 from "../assets/home_7.jpg"
import home_8 from "../assets/home_8.jpg"

// View contents based on whether a user is logged in or a new user
const LoggedInHomePage = () => {
    const [name, setName] = useState('')

    let accessToken = localStorage.getItem('REACT_TOKEN_AUTH_KEY')
    let userId = localStorage.getItem('id')

    const headers = {
        'Authorization': `Bearer ${JSON.parse(accessToken)}`
    }

    useEffect(() => {
        axios.get(`/user/${userId}`, { headers: headers })
            .then(response => {
                console.log("Home page: Success fetching the user profile.")
                console.log(response.data)
                setName(response.data.Firstname)
            }).catch(error => {
                console.log("Home page: Error occured while fetching user profile.")
                console.log(error.response)

                // Fetching refresh token when token expires.
                if (error.response.status == 401) {
                    console.log("Home page: Retrying to log in the user")
                    let refreshToken = localStorage.getItem('REACT_TOKEN_REFRESH_KEY')

                    if (!refreshToken) {
                        logout()
                        localStorage.clear()
                        return
                    }
                    const refresh_headers = {
                        'Authorization': `Bearer ${JSON.parse(refreshToken)}`
                    }
                    axios.post('/user/token/refresh', {}, { headers: refresh_headers })
                        .then(response => {
                            console.log("Home page: Success from fetching refresh token from /refresh endpoint")
                            console.log(response.data)
                            login(response.data.access_token)
                            const reload = window.location.reload()
                            reload()
                        })
                        .catch(error => {
                            console.log("Home page: Error occured during token refresh. myaccount.js")
                            console.log(error.response)
                        })
                }
            })
    }, [])

    return (
        <>
            <div class="text-center bg-image" style={{ backgroundImage: `url(${foodBackground})`, marginTop: '50px' }}>
                <div class="mask" style={{ backgroundColor: 'rgba(0, 0, 0, 0.7', height: '800px' }}>
                    <div class="d-flex justify-content-center h-50">
                        <div class="text-white">
                            <h1 class="mb-3" style={{ fontWeight: 'bold', marginTop: '70px' }}>Hi, {name}!</h1>
                            <h1 class="mb-3" style={{ fontWeight: 'bold' }}>Welcome back to AssistWise</h1>
                            <div style={{ display: 'flex', flexDirection: 'row', alignItems: 'center' }}>
                                <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
                                    <a href='/recommendations/food'>
                                        <img style={{ width: 300, height: 400, borderRadius: 20 }} src={foodRecommendation} class="card-img-top" alt="Banana bread ." />
                                    </a>
                                    <Link style={{ borderRadius: 20, fontWeight: 'bold' }} to='/recommendations/food' className="btn btn-outline-light btn-lg m-4">RECIPE RECOMMENDATIONS</Link>
                                </div>
                                <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
                                    <a href='/recommendations/water'>
                                        <img style={{ width: 250, height: 400, borderRadius: 20 }} src={waterRecommendation} class="card-img-top" alt="Water" />
                                    </a>
                                    <Link style={{ borderRadius: 20, fontWeight: 'bold' }} to='/recommendations/water' className="btn btn-outline-light btn-lg m-4">EVERYDAY HYDRATION</Link>
                                </div>
                                <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
                                    <a href='/recommendations/activity'>
                                        <img style={{ width: 450, height: 400, borderRadius: 20, marginLeft: 30 }} src={activity} class="card-img-top" alt="Activity" />
                                    </a>
                                    <Link style={{ borderRadius: 20, fontWeight: 'bold' }} to='/recommendations/activity' className="btn btn-outline-light btn-lg m-4">LEISURE ACTIVITIES</Link>
                                </div>
                            </div>
                        </div>

                    </div>
                </div>
            </div>
        </>
    )
}

const NewUserHomePage = () => {
    return (
        <>
            <div class="text-center bg-image" style={{ backgroundImage: `url(${homeImage})`, marginTop: '66px', height: '800px' }}>
                <div class="mask" style={{ backgroundColor: 'rgba(0, 0, 0, 0.7)', height: '800px' }}>
                    <div class="d-flex justify-content-center align-items-center h-50">
                        <div class="text-white">
                            <h1 class="mb-3" style={{ fontWeight: 'bold' }}>Welcome to AssistWise</h1>
                            <h3 class="mb-3">Let's begin your personalized recommendations journey.</h3>
                            <h5 class="mb-4">Get on board and sign-up here to receive expert recommendations tailored to your needs.</h5>
                            <Link to='/signup' className="btn btn-outline-light btn-lg m-2">GET STARTED NOW</Link>
                        </div>
                    </div>
                </div>
            </div>
            <div class="row" style={{ backgroundColor: 'rgba(0, 0, 0, 0.7)' }}>
                <div>
                    <br></br>
                    <h2 style={{ textAlign: 'center', fontWeight: 'bold', color: 'white' }}>Discover food recommendations for various meal occasions, such as Breakfast, Morning Snack, Lunch, Afternoon Snack, and Dinner.</h2>
                    <br></br>
                </div>
                <div class="col-lg-4 col-md-12 mb-4 mb-lg-0" style={{ paddingLeft: '20px' }}>
                    <img src={home_6} class="w-100 shadow-1-strong rounded mb-4" alt="Vegetable salad" />
                    <img src={home_7} class="w-100 shadow-1-strong rounded mb-4" alt="Muffins" />

                </div>
                <div class="col-lg-4 mb-4 mb-lg-0" style={{ paddingLeft: '1px', paddingRight: '1px' }}>
                    <img src={home_2} class="w-100 shadow-1-strong rounded mb-4" alt="Egg on pan" />
                    <img src={home_3} class="w-100 shadow-1-strong rounded mb-4" alt="Smoothies" />
                    <img src={home_1} class="w-100 shadow-1-strong rounded mb-4" alt="Chopping greens" />
                </div>
                <div class="col-lg-4 mb-4 mb-lg-0" style={{ paddingRight: '20px' }}>
                    <img src={home_8} class="w-100 shadow-1-strong rounded mb-4" alt="Strawberry smoothie" />
                    <img src={home_5} class="w-100 shadow-1-strong rounded mb-4" alt="Bread omlete" />
                </div>
            </div>
        </>
    )
}

const HomePage = () => {
    const [isUserLoggedIn] = useAuth()
    return (
        <>
            {isUserLoggedIn ? <LoggedInHomePage /> : <NewUserHomePage />}
        </>
    )
}

export default HomePage