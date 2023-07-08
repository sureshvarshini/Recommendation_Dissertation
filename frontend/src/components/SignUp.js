import React, { useState } from 'react'
import { Form, Button } from 'react-bootstrap'
import { Link } from 'react-router-dom'
import { useForm } from 'react-hook-form'

const SignupPage = () => {
    const [username, setUsername] = useState('')
    const [email, setEmail] = useState('')
    const [password, setPassword] = useState('')
    const [confirmPassword, setConfirmPassword] = useState('')
    const [firstname, setFirstName] = useState('')
    const [lastname, setLastName] = useState('')
    const [age, setAge] = useState('')
    const [gender, setGender] = useState('')
    const [height, setHeight] = useState('')
    const [weight, setWeight] = useState('')
    const [illness, setIllness] = useState('')

    const { register, watch, handleSubmit, reset, formState: { errors } } = useForm()

    const signupSubmitForm = (data) => {
        console.log("Sign-Up form submitted with below details.")
        const formData = {
            gender:gender,
            illness:illness
        }
        console.log({...data,...formData})

        if (data.password === data.confirmPassword) {
            const requestOptions = {
                mode:'cors',
                method: "POST",
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({...data,...formData})
            }

            fetch('http://localhost:5000/user/signup', requestOptions)
            .then(response => response.json)
            .then(data => console.log(data))
            .catch(error => console.log(error))
            reset()
        }
        else {
            alert("Passwords dont match. Please try again.")
        }
    }

    console.log(watch("username"))

    return (
        <div className="container">
            <div className="form">
                <h1>Get on board and sign-up here to receive expert recommendations tailored to your needs.</h1>
                <form>
                    <Form.Group>
                        <Form.Label>Username</Form.Label>
                        <Form.Control type="text" placeholder="Your username here."
                            {...register("username", {
                                required: true,
                                validate: {
                                    matchPattern: (v) => /^[a-zA-Z0-9_]+$/.test(v)
                                }
                            })}
                        />
                        {errors.username?.type === "required" && <span style={{ color: "red", fontSize: 14 }}>username is required</span>}
                        {errors.username?.type === "matchPattern" && <span style={{ color: "red", fontSize: 14 }}>username can contain only letters, numbers and _ (underscore)</span>}
                    </Form.Group>
                    <br></br>
                    <Form.Group>
                        <Form.Label>Email</Form.Label>
                        <Form.Control type="email" placeholder="Your email address here."
                            {...register("email", {
                                required: true,
                                validate: {
                                    matchPattern: (v) =>
                                        /^\w+([.-]?\w+)*@\w+([.-]?\w+)*(\.\w{2,3})+$/.test(v)
                                }
                            })}
                        />
                        {errors.email?.type === "required" && <span style={{ color: "red", fontSize: 14 }}>email is required</span>}
                        {errors.email?.type === "matchPattern" && <span style={{ color: "red", fontSize: 14 }}>email address should be valid</span>}
                    </Form.Group>
                    <br></br>
                    <Form.Group>
                        <Form.Label>Password</Form.Label>
                        <Form.Control type="password" placeholder="Your password here."
                            {...register("password", { required: true, minLength: 6, maxLength: 18 })}
                        />
                        {errors.password?.type === "required" && <span style={{ color: "red", fontSize: 14 }}>password is required</span>}
                        {errors.password?.type === "minLength" && <span style={{ color: "red", fontSize: 14 }}>password should have minimum of 6 characters</span>}
                        {errors.password?.type === "maxLength" && <span style={{ color: "red", fontSize: 14 }}>password cannot exceed 18 characters</span>}
                    </Form.Group>
                    <br></br>
                    <Form.Group>
                        <Form.Label>Confirm password</Form.Label>
                        <Form.Control type="password" placeholder="Your password here."
                            {...register("confirmPassword", { required: true, minLength: 6, maxLength: 18 })}
                        />
                        {errors.confirmPassword?.type === "required" && <span style={{ color: "red", fontSize: 14 }}>confirm password field is required</span>}
                        {errors.confirmPassword?.type === "minLength" && <span style={{ color: "red", fontSize: 14 }}>confirm password should have minimum of 6 characters</span>}
                        {errors.confirmPassword?.type === "maxLength" && <span style={{ color: "red", fontSize: 14 }}>confirm password cannot exceed 18 characters</span>}
                    </Form.Group>
                    <br></br>
                    <Form.Group>
                        <Form.Label>First Name</Form.Label>
                        <Form.Control type="text" placeholder="Your first name here."
                            {...register("firstname", { required: true, minLength: 3, maxLength: 50 })}
                        />
                        {errors.firstname?.type === "required" && <span style={{ color: "red", fontSize: 14 }}>firstname is required</span>}
                        {errors.firstname?.type === "minLength" && <span style={{ color: "red", fontSize: 14 }}>firstname should have minimum of 3 characters</span>}
                        {errors.firstname?.type === "maxLength" && <span style={{ color: "red", fontSize: 14 }}>firstname cannot exceed 50 characters</span>}
                    </Form.Group>
                    <br></br>
                    <Form.Group>
                        <Form.Label>Last Name</Form.Label>
                        <Form.Control type="text" placeholder="Your last name here."
                            {...register("lastname", { required: true, minLength: 3, maxLength: 50 })}
                        />
                        {errors.lastname?.type === "required" && <span style={{ color: "red", fontSize: 14 }}>lastname is required</span>}
                        {errors.lastname?.type === "minLength" && <span style={{ color: "red", fontSize: 14 }}>lastname should have minimum of 3 characters</span>}
                        {errors.lastname?.type === "maxLength" && <span style={{ color: "red", fontSize: 14 }}>lastname cannot exceed 50 characters</span>}
                    </Form.Group>
                    <br></br>
                    <Form.Group>
                        <Form.Label>Age</Form.Label>
                        <Form.Control type="number" placeholder="Your age here." min='1' max='150'
                            {...register("age", { required: true, valueAsNumber: true })}
                        />
                        {errors.age?.type === "required" && <span style={{ color: "red", fontSize: 14 }}>age is required</span>}
                    </Form.Group>
                    <br></br>
                    <Form.Group controlId="formBasicSelect1">
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
                            {...register("height", { required: true, valueAsNumber: true })}
                        />
                        {errors.height?.type === "required" && <span style={{ color: "red", fontSize: 14 }}>height is required</span>}
                    </Form.Group>
                    <br></br>
                    <Form.Group>
                        <Form.Label>Weight</Form.Label>
                        <Form.Control type="number"
                            min='1'
                            placeholder="Your weight here (in kg)."
                            {...register("weight", { required: true, valueAsNumber: true })}
                        />
                        {errors.weight?.type === "required" && <span style={{ color: "red", fontSize: 14 }}>weight is required</span>}
                    </Form.Group>
                    <br></br>
                    <Form.Group controlId="formBasicSelect2">
                        <Form.Label>Illness</Form.Label>
                        <Form.Control as="select"
                            value={illness}
                            name="illness"
                            onChange={(event) => { setIllness(event.target.value) }}>
                            <option>Select illness (if any, else select 'No').</option>
                            <option value={"Illness 1"}>Illness 1</option>
                            <option value={"No"}>No</option>
                        </Form.Control>
                    </Form.Group>
                    <br></br>
                    <Form.Group>
                        <Button as="sub" variant="primary" onClick={handleSubmit(signupSubmitForm)}>
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