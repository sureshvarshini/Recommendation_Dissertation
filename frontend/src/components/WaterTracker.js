import React, { useEffect, useState } from 'react'
import { Button } from 'react-bootstrap'
import axios from 'axios'
import '../css/WaterTracker.css'
import water from "../assets/water.jpg"

const WaterTrackerPage = () => {
    const [waterIntakeStatus, setWaterIntakeStatus] = useState('')
    const [waterIntakeDetails, setWaterIntakeDetails] = useState('')
    let userId = localStorage.getItem('id')

    const logWater = (data) => {
        console.log(data)
        const waterData = {
            amount: data,
        }
        const body = JSON.stringify(waterData)
        const headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }

        axios.post(`/water/${userId}`, body, { headers: headers })
            .then(response => {
                console.log("Success upadting water details.")
                console.log(response.data)
                const reload = window.location.reload()
            })
            .catch(error => {
                console.log("Error occured from fetching water details.")
                console.log(error.response.data)
            })
    }

    // Get water intake details from flask endpoint
    useEffect(() => {
        axios.get(`/water/${userId}`)
            .then(response => {
                console.log("Success fetching the food recommendations.")
                console.log(response.data)
                setWaterIntakeStatus(response.data.water_status_code)
                setWaterIntakeDetails(response.data)
            }).catch(error => {
                console.log("Error occured while fetching the recommended foods.")
                console.log(error.response)
            })
    }, [])

    return (
        <div className='container justify-content-center align-items-center' style={{ padding: 10 }}>
            <div className='card d-flex align-items-center'>
                <img className='card-image' src={water} alt='water' />
                <div className='card-header'>
                    <div className='card-title-group'>
                        {waterIntakeStatus == -1 &&
                            <>
                                <h5 className='card-title'>7 cups left</h5>
                                <div className='card-text fst-italic'>Start Drinking! ({waterIntakeDetails.remaining_ml}ml remaining)</div>
                                <small>Goal: 7 cups (1700ml)</small>
                            </>
                        }
                        {waterIntakeStatus == 0 &&
                            <>
                                <h5 className='card-title'>{waterIntakeDetails.remaining_cups} cups left </h5>
                                <div className='card-text fst-italic'>Keep Drinking! ({waterIntakeDetails.remaining_ml}ml remaining)</div>
                                <small>Goal: 7 cups (1700ml)</small>
                            </>
                        }
                        {waterIntakeStatus == 1 &&
                            <>
                                <h5 className='card-title'>DAILY GOAL reached!</h5>
                                <div className='card-text fst-italic'>HURRAY, Keep it up!</div>
                            </>
                        }
                    </div>
                </div>
            </div>

            <form style={{ padding: 50 }}>
                <h3>Log your water intake here (ml).</h3>
                <Button as="sub" variant="primary" class="btn btn-primary btn-block btn-lg" style={{ margin: 10 }} onClick={() => logWater(100)}>100 ml</Button>
                <Button as="sub" variant="primary" class="btn btn-primary btn-block btn-lg" style={{ margin: 10 }} onClick={() => logWater(250)}>250 ml (1 cup)</Button>
                <Button as="sub" variant="primary" class="btn btn-primary btn-block btn-lg" style={{ margin: 10 }} onClick={() => logWater(500)}>500 ml (2 cups)</Button>
                <Button as="sub" variant="primary" class="btn btn-primary btn-block btn-lg" style={{ margin: 10 }} onClick={() => logWater(750)}>750 ml (3 cups)</Button>
                <Button as="sub" variant="primary" class="btn btn-primary btn-block btn-lg" style={{ margin: 10 }} onClick={() => logWater(1000)}>1000 ml (4 cups)</Button>
                <Button as="sub" variant="primary" class="btn btn-primary btn-block btn-lg" style={{ margin: 10 }} onClick={() => logWater(1250)}>1250 ml (5 cups)</Button>
                <Button as="sub" variant="primary" class="btn btn-primary btn-block btn-lg" style={{ margin: 10 }} onClick={() => logWater(1500)}>1500 ml (6 cups)</Button>
                <Button as="sub" variant="primary" class="btn btn-primary btn-block btn-lg" style={{ margin: 10 }} onClick={() => logWater(1750)}>1750 ml (7 cups)</Button>
            </form>
        </div>

    )
}

export default WaterTrackerPage