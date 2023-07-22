import React, { useEffect, useState } from 'react'
import { Form, Button, Modal } from 'react-bootstrap'
import { Link, useNavigate } from 'react-router-dom'
import { useForm } from 'react-hook-form'
import axios from 'axios'
import { logout } from '../Auth'

const WaterTrackerPage = () => {
    const [waterIntakeStatus, setWaterIntakeStatus] = useState('')
    const [waterIntakeDetails, setWaterIntakeDetails] = useState('')
    const { register, watch, handleSubmit, reset, formState: { errors } } = useForm()
    const navigate = useNavigate()
    let userId = localStorage.getItem('id')

    const logWater = (data) => {
        console.log('yuhoo!')
        console.log(data)
        const body = JSON.stringify(data)
        const headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }

        axios.post(`/water/${userId}`, body, { headers: headers })
            .then(response => {
                console.log("Success from fetching water details.")
                console.log(response.data)
                
                reset()
                navigate('/recommendations/water')
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
        <div className='container'>
            {waterIntakeStatus == -1 &&
                <div>You havent started logging yout water intake.
                    <form>
                        <Form.Group>
                            <Form.Label>Log your water intake here (ml)</Form.Label>
                            <Form.Control type="number"
                                min='1'
                                {...register("amount", { valueAsNumber: true })}
                            />
                        </Form.Group>
                        <Form.Group>
                            <Button as="sub" variant="primary" onClick={handleSubmit(logWater)}>Log water</Button>
                        </Form.Group>
                    </form>
                </div>}

            {waterIntakeStatus == 0 &&
                <h2>Keep drinking! <br></br>You still have {waterIntakeDetails.remaining_cups} cups to drink for the day.
                    <br></br>
                    <form>
                        <Form.Group>
                            <Form.Label>Log your water intake here (ml)</Form.Label>
                            <Form.Control type="number"
                                min='1'
                                {...register("amount", { valueAsNumber: true })}
                            />
                        </Form.Group>
                        <Form.Group>
                            <Button as="sub" variant="primary" onClick={handleSubmit(logWater)}>Log water</Button>
                        </Form.Group>
                    </form>
                </h2>}

            {waterIntakeStatus == 1 &&
                <h2>Hurray! You have reached your daily water intake goal!
                    <p>Take me <Link to='/'>home</Link></p>
                </h2>


            }
        </div>
    )
}

export default WaterTrackerPage