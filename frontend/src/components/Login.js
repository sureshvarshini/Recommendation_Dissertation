import React, { useState } from "react"
import { Form, Button } from 'react-bootstrap'
import { Link } from "react-router-dom"

const LoginPage = () => {

    const [username, setUsername] = useState('')
    const [password, setPassword] = useState('')

    const loginSubmitForm = () => {
        console.log("Logged form submitted.")
        console.log("Following details were entered:")
        console.log("Username:", username)
        console.log("Password:", password)
    }

    return(
        <div className="container">
            <div className="form">
                <h1>Get your tailored recommended content by logging in here.</h1>
                <form>
                    <Form.Group>
                        <Form.Label>Username</Form.Label>
                        <Form.Control type="text"
                            value={username}
                            name="username"
                            onChange={(event) => { setUsername(event.target.value) }}
                        />
                    </Form.Group>
                    <br></br>
                    <Form.Group>
                        <Form.Label>Password</Form.Label>
                        <Form.Control type="password"
                            value={password}
                            name="password"
                            onChange={(event) => { setPassword(event.target.value) }}
                        />
                    </Form.Group>                    
                    <br></br>
                    <Form.Group>
                        <Button as="sub" variant="primary" onClick={loginSubmitForm}>
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