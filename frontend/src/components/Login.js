import React, { useState } from 'react'
import { Form, Button, Alert } from 'react-bootstrap'
import { Link, useNavigate } from 'react-router-dom'
import { useForm } from 'react-hook-form'
import axios from 'axios'
import { login } from '../Auth'

const LoginPage = () => {
    const [responseData, setResponseData] = useState('')
    const [variant, setVariant] = useState('')
    const [show, setShow] = useState(false)

    const { register, watch, handleSubmit, reset, formState: { errors } } = useForm()

    const navigate = useNavigate()

    // Hit flask API
    const loginSubmitForm = (data) => {
        console.log("Logged user form submitted. Following details were entered:")
        console.log(data)

        const body = JSON.stringify(data)
        const headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }

        axios.post('/user/login', body, { headers: headers })
            .then(response => {
                console.log("Success from fetching from signup endpoint")
                console.log(response.data)
                setResponseData(response.data.access_token)
                login(response.data.access_token)

                // Page you want re-direct to after login - right now its home page
                navigate('/')
            })
            .catch(error => {
                console.log("Error occured from fetching from login endpoint.")
                console.log(error.response.data)
                setResponseData(error.response.data)
                // Show error message if login failed
                setShow(true)
                setVariant("danger")
            })

        reset()
    }

    return (
        <div className="container">
            <div className="form">
                <h1>Get your tailored recommended content by logging in here.</h1>
                <form>
                    <Form.Group>
                        <Form.Label>Username</Form.Label>
                        <Form.Control type="text"
                            {...register("username", { required: true })}
                        />
                        {errors.username?.type === "required" && <span style={{ color: "red", fontSize: 14 }}>username is required</span>}
                    </Form.Group>
                    <br></br>
                    <Form.Group>
                        <Form.Label>Password</Form.Label>
                        <Form.Control type="password"
                            {...register("password", { required: true })}
                        />
                        {errors.password?.type === "required" && <span style={{ color: "red", fontSize: 14 }}>password is required</span>}
                    </Form.Group>
                    <br></br>
                    {show ?
                        <>
                            <Alert key={variant} variant={variant} onClose={() => { setShow(false) }} dismissible>
                                <p>{responseData.message}</p>
                            </Alert>
                        </>
                        : <br></br>
                    }
                    <Form.Group>
                        <Button as="sub" variant="primary" onClick={handleSubmit(loginSubmitForm)}>
                            Login
                        </Button>
                    </Form.Group>
                    <br></br>
                    <Form.Group>
                        <small>
                            New user? Signup <Link to='/signup'>here</Link> to unlock your tailored recommendations and begin your journey.
                        </small>
                    </Form.Group>
                </form>
            </div>
        </div>
    )
}

export default LoginPage