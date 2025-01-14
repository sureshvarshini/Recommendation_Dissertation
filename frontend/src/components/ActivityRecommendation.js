import React, { useEffect, useState } from 'react'
import { Rating } from 'react-simple-star-rating'
import { Link } from 'react-router-dom'
import { Modal } from 'react-bootstrap'
import Slider from 'react-slick';
import axios from 'axios'
import ActivityCard from './ActivityCard'
import 'slick-carousel/slick/slick.css';
import 'slick-carousel/slick/slick-theme.css';

const ActivityRecommendationPage = () => {
    const [schedule, setSchedule] = useState([])
    const [morningActivity, setMorningActivity] = useState([])
    const [afternoonActivity, setAfternoonActivity] = useState([])
    const [eveningActivity, setEveningActivity] = useState([])
    const [selectedActivity, setSelectedActivity] = useState([])
    const [done, setDone] = useState(undefined)
    const [repetitions, setRepetitions] = useState([])
    const [directions, setDirections] = useState([])
    const [show, setShow] = useState('')
    const [rating, setRating] = useState(0)
    const [previousRating, setPreviousRating] = useState('')

    let userId = localStorage.getItem('id')

    const closeModal = () => {
        setShow(false)
    }

    const showModal = (activity) => {
        console.log('Activity card clicked.')
        console.log(activity)
        setSelectedActivity(activity)
        setRepetitions((activity.repetitions).split('.,'))
        setDirections((activity.directions).split('.,'))
        setShow(true)

        // // Get the ratings - to view when food card is clicked
        // axios.get(`/ratings/${userId}/${recipe.id}`)
        //     .then(response => {
        //         console.log("Success fetching rating for food.")
        //         console.log(response.data)
        //         setPreviousRating(response.data.rating)
        //     }).catch(error => {
        //         console.log("Error occured while fetching rating for food.")
        //         console.log(error.response)
        //     })
    }

    const handleRating = (rating) => {
        console.log('Rating clicked.')
        console.log(rating)
        setRating(rating)

        const data = {
            rating: rating,
            user_id: parseInt(userId),
            food_id: selectedActivity.id
        }
        const headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        const body = JSON.stringify(data)

        console.log(body)
        axios.post('/ratings', body, { headers: headers })
            .then(response => {
                console.log("Success updating rating of food.")
                console.log(response.data)
            }).catch(error => {
                console.log("Error occured while updating rating of food profile.")
                console.log(error.response)
            })
    }

    useEffect(() => {
        axios.get(`/schedule/${userId}`)
            .then(response => {
                console.log("Success fetching user schedule for the day.")
                console.log(response.data)
                setSchedule(response.data.schedule)
                setDone(true)
            }).catch(error => {
                console.log("Error occured while fetching user schedule for the day.")
                console.log(error.response)
            })

        axios.get(`/activity/${userId}`)
            .then(response => {
                console.log("Success fetching activities.")
                console.log(response.data)
                setMorningActivity(response.data.activities.Morning)
                setAfternoonActivity(response.data.activities.Afternoon)
                setEveningActivity(response.data.activities.Evening)
            }).catch(error => {
                console.log("Error occured while fetching activities.")
                console.log(error.response)
            })
    }, [])

    const settings = {
        dots: true,
        infinite: true,
        slidesToShow: 2,
        slidesToScroll: 2,
        nextArrow: (
            <div>
                <div className="next-slick-arrow"> ⫸ </div>
            </div>
        ),
        prevArrow: (
            <div>
                <div className="prev-slick-arrow"> ⫷ </div>
            </div>
        )
    };

    const settings_one = {
        dots: true,
        infinite: true,
        slidesToShow: 1,
        slidesToScroll: 1,
        nextArrow: (
            <div>
                <div className="next-slick-arrow"> ⫸ </div>
            </div>
        ),
        prevArrow: (
            <div>
                <div className="prev-slick-arrow"> ⫷ </div>
            </div>
        )
    };


    return (
        <div className='container'>
            <Modal show={show} size="lg" onHide={closeModal} style={{ padding: 150 }}>
                <Modal.Header closeButton>
                    <Modal.Title style={{ fontWeight: 'bold' }}>
                        {selectedActivity.name}
                    </Modal.Title>
                </Modal.Header>
                {selectedActivity && selectedActivity.type && (selectedActivity.type.includes('exercise') || selectedActivity.type.includes('Yoga')) &&
                    <img className='activity-card-image' src={selectedActivity.image} alt={selectedActivity.name} style={{ width: "auto", height: "auto" }} />}
                <Modal.Body style={{ fontSize: '20px' }}>
                    <p style={{ fontWeight: 'bold' }}>Directions:</p>
                    <ul>
                        {directions.map((i, index) => (
                            <li key={index}>{i}</li>
                        ))}
                    </ul>
                    <p style={{ fontWeight: 'bold' }}>Repetitions:</p>
                    <ul>
                        {repetitions.map((i, index) => (
                            <li key={index}>{i}</li>
                        ))}
                    </ul>
                </Modal.Body>
            </Modal>
            <div class="d-flex justify-content-center">
                <h3 style={{ fontWeight: 'bold', marginTop: '50px', textAlign: "center" }}>Greetings!! Get a glimpse of your recommended daily schedule right here.</h3>
            </div>
            {!done ? (
                <div class="d-flex justify-content-left">
                    <small>Loading....</small>
                    <div class="spinner-grow spinner-grow-sm text-primary" role="status">
                        <span class="sr-only"></span>
                    </div>
                    <div class="spinner-grow spinner-grow-sm text-secondary" role="status">
                        <span class="sr-only"></span>
                    </div>
                    <div class="spinner-grow spinner-grow-sm text-success" role="status">
                        <span class="sr-only"></span>
                    </div>
                    <div class="spinner-grow spinner-grow-sm text-danger" role="status">
                        <span class="sr-only"></span>
                    </div>
                    <div class="spinner-grow spinner-grow-sm text-warning" role="status">
                        <span class="sr-only"></span>
                    </div>
                    <div class="spinner-grow spinner-grow-sm text-info" role="status">
                        <span class="sr-only"></span>
                    </div>
                    <div class="spinner-grow spinner-grow-sm text-light" role="status">
                        <span class="sr-only"></span>
                    </div>
                </div>
            ) : (
                <div className='activity'>
                    {Object.entries(schedule).map(([activity, time]) => (
                        <div key={activity}>
                            {time.length > 0 && (
                                <h2 style={{ marginTop: '30px', backgroundColor: '#cafaac', borderRadius: '10px', padding: 10, fontWeight: 'bold' }}>
                                    {activity} - {time.map(hour => (
                                        <span key={hour}>
                                            {hour > 12 ? `${hour - 12} PM` : `${hour} AM`}
                                            {time.indexOf(hour) !== time.length - 1 ? ', ' : ''}
                                        </span>
                                    ))}
                                </h2>
                            )}
                            {(activity === 'Breakfast' || activity === 'Morning Snacks' || activity === 'Lunch' || activity === 'Afternoon Snacks' || activity === "Dinner") &&
                                <div className='sub-activity'>
                                    <h3 style={{ marginTop: '30px', padding: 10 }}>Lead me to today's suggested dishes! Click <Link to='/recommendations/food' style={{ fontWeight: 'bold' }}>here</Link></h3>
                                </div>
                            }
                            {activity === 'Morning' &&
                                <div className='sub-activity'>
                                    {Object.keys(morningActivity).map((type) => {
                                        if (morningActivity[type].length > 0 && time.length > 0) {
                                            return (
                                                <div key={type}>
                                                    <h3 style={{ marginTop: '30px', padding: 10, fontWeight: 'bold' }}>{type}</h3>
                                                    {morningActivity[type].length == 1 ? (
                                                        <Slider {...settings_one}>
                                                            {morningActivity[type].map((activity) => (
                                                                <div key={activity.id}>
                                                                    <ActivityCard
                                                                        Name={activity.name}
                                                                        Type={activity.type}
                                                                        Image={activity.image}
                                                                        onClick={() => { showModal(activity) }}
                                                                    />
                                                                </div>
                                                            ))}
                                                        </Slider>
                                                    ) : (
                                                        <Slider {...settings}>
                                                            {morningActivity[type].map((activity) => (
                                                                <div key={activity.id}>
                                                                    <ActivityCard
                                                                        Name={activity.name}
                                                                        Type={activity.type}
                                                                        Image={activity.image}
                                                                        onClick={() => { showModal(activity) }}
                                                                    />
                                                                </div>
                                                            ))}
                                                        </Slider>
                                                    )}
                                                </div>
                                            )
                                        }
                                        return null
                                    })}
                                </div>
                            }
                            {activity === 'Afternoon' &&
                                <div className='sub-activity'>
                                    {Object.keys(afternoonActivity).map((type) => {
                                        if (afternoonActivity[type].length > 0 && time.length > 0) {
                                            return (
                                                <div key={type}>
                                                    <h3 style={{ marginTop: '30px', padding: 10, fontWeight: 'bold' }}>{type}</h3>
                                                    <Slider {...settings_one}>
                                                        {afternoonActivity[type].map((activity) => (
                                                            <div key={activity.id}>
                                                                <ActivityCard
                                                                    Name={activity.name}
                                                                    Type={activity.type}
                                                                    Image={activity.image}
                                                                    onClick={() => { showModal(activity) }}
                                                                />
                                                            </div>
                                                        ))}
                                                    </Slider>
                                                </div>
                                            )
                                        }
                                        return null
                                    })}
                                </div>
                            }
                            {activity === 'Evening' &&
                                <div className='sub-activity'>
                                    {Object.keys(eveningActivity).map((type) => {
                                        if (eveningActivity[type].length > 0 && time.length > 0) {
                                            return (
                                                <div key={type}>
                                                    {type.includes('Yoga') ?
                                                        (<h3 style={{ marginTop: '30px', padding: 10, fontWeight: 'bold' }}>{type} - Kindly adhere to the sequence of cards for a complete yoga session.</h3>) :
                                                        (<h3 style={{ marginTop: '30px', padding: 10, fontWeight: 'bold' }}>{type}</h3>)}
                                                    {eveningActivity[type].length == 1 ? (
                                                        <Slider {...settings_one}>
                                                            {eveningActivity[type].map((activity) => (
                                                                <div key={activity.id}>
                                                                    <ActivityCard
                                                                        Name={activity.name}
                                                                        Type={activity.type}
                                                                        Image={activity.image}
                                                                        onClick={() => { showModal(activity) }}
                                                                    />
                                                                </div>
                                                            ))}
                                                        </Slider>
                                                    ) : (
                                                        <Slider {...settings}>
                                                            {eveningActivity[type].map((activity) => (
                                                                <div key={activity.id}>
                                                                    <ActivityCard
                                                                        Name={activity.name}
                                                                        Type={activity.type}
                                                                        Image={activity.image}
                                                                        onClick={() => { showModal(activity) }}
                                                                    />
                                                                </div>
                                                            ))}
                                                        </Slider>
                                                    )}
                                                </div>
                                            )
                                        }
                                        return null
                                    })}
                                </div>
                            }
                        </div>
                    ))}
                </div>
            )}
        </div >
    )
}

export default ActivityRecommendationPage