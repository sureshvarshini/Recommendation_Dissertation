import React, { useState } from 'react'
import { Form, Button } from 'react-bootstrap'
import { Link } from 'react-router-dom'
import { useForm } from 'react-hook-form'

const SignupPage = () => {
    const [username, setUsername] = useState('')
    const [email, setEmail] = useState('')
    const [password, setPassword] = useState('')
    const [confirmPassword, setConfirmPassword] = useState('')
    const [name, setName] = useState('')
    const [age, setAge] = useState('')
    const [gender, setGender] = useState('')
    const [height, setHeight] = useState('')
    const [weight, setWeight] = useState('')
    const [illness, setIllness] = useState('')

    const { register, watch, handleSubmit, formState: { errors } } = useForm()

    const signupSubmitForm = () => {
        console.log("Sign-Up form submitted.")
        console.log("Following details were entered:")
        console.log("Username:", username)
        console.log("Email:", email)
        console.log("Name:", name)
        console.log("Age:", age)
        console.log("Gender:", gender)
        console.log("Height:", height)
        console.log("Weight:", weight)
        console.log("Illness:", illness)
    }

    return (
        <div className="container">
            <div className="form">
                <h1>Get on board and sign-up here to receive expert recommendations tailored to your needs.</h1>
                <form>
                    <Form.Group>
                        <Form.Label>Username</Form.Label>
                        <Form.Control type="text" placeholder="Your username here."
                            {...register("username", { required: true })}
                        />
                    </Form.Group>
                    <br></br>
                    <Form.Group>
                        <Form.Label>Email</Form.Label>
                        <Form.Control type="email" placeholder="Your email address here."
                            {...register("email", { required: true })}
                        />
                    </Form.Group>
                    <br></br>
                    <Form.Group>
                        <Form.Label>Password</Form.Label>
                        <Form.Control type="password" placeholder="Your password here."
                            {...register("password", { required: true, minLength: 6, maxLength: 18 })}
                        />
                    </Form.Group>
                    <br></br>
                    <Form.Group>
                        <Form.Label>Confirm password</Form.Label>
                        <Form.Control type="password" placeholder="Your password here."
                            {...register("confirmPassword", { required: true, minLength: 6, maxLength: 18 })}
                        />
                    </Form.Group>
                    <br></br>
                    <Form.Group>
                        <Form.Label>Name</Form.Label>
                        <Form.Control type="text" placeholder="Your good name here."
                        {...register("name", { required: true, minLength: 3, maxLength: 50 })}
                        />
                    </Form.Group>
                    <br></br>
                    <Form.Group>
                        <Form.Label>Age</Form.Label>
                        <Form.Control type="number" placeholder="Your age here."
                            {...register("age", { required: true, minLength: 1, maxLength: 150 })}
                        />
                    </Form.Group>
                    <br></br>
                    <Form.Group controlId="formBasicSelect">
                        <Form.Label>Gender</Form.Label>
                        <Form.Control as="select"
                            value={gender}
                            name="gender"
                            onChange={(event) => { setGender(event.target.value) }}>
                            <option>Select which suits you.</option>
                            <option value={"Male"}>Male</option>
                            <option value={"Female"}>Female</option>
                        </Form.Control>
                    </Form.Group>
                    <br></br>
                    <Form.Group>
                        <Form.Label>Height</Form.Label>
                        <Form.Control type="number"
                            min='1'
                            placeholder="Your height here (in cm)."
                            value={height}
                            name="height"
                            onChange={(event) => { setHeight(event.target.value) }}
                        />
                    </Form.Group>
                    <br></br>
                    <Form.Group>
                        <Form.Label>Weight</Form.Label>
                        <Form.Control type="number"
                            min='1'
                            placeholder="Your weight here (in kg)."
                            value={weight}
                            name="weight"
                            onChange={(event) => { setWeight(event.target.value) }}
                        />
                    </Form.Group>
                    <br></br>
                    // need to add options for illness
                    <Form.Group>
                        <Form.Label>Illness</Form.Label>
                        <Form.Control type="text" placeholder="State your illness (if any) here."
                            value={illness}
                            name="illness"
                            onChange={(event) => { setIllness(event.target.value) }}
                        />
                    </Form.Group>
                    <br></br>
                    <Form.Group>
                        <Button as="sub" variant="primary" onClick={signupSubmitForm}>
                            Signup
                        </Button>
                    </Form.Group>
                    <br></br>
                    <Form.Group>
                        <small>
                            Existing user? Sign in <Link to='/login'>here</Link> to pick up where you left off and view your tailored recommendations.
                        </small>
                    </Form.Group>
                </form>
            </div>
        </div>
    )
}

export default SignupPage