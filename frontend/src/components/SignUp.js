import React, { useState } from 'react'
import { Form, Button, Alert } from 'react-bootstrap'
import RangeSlider from 'react-bootstrap-range-slider'
import { Link } from 'react-router-dom'
import { useForm } from 'react-hook-form'
import axios from 'axios'
import 'bootstrap/dist/css/bootstrap.css'
import 'react-bootstrap-range-slider/dist/react-bootstrap-range-slider.css'
import signupImage from "../assets/signup.jpg"

const SignupPage = () => {
    const [gender, setGender] = useState('')
    const [illness, setIllness] = useState('')
    const [mobilityscore, setMobilityscore] = useState(1)
    const [dexterityscore, setDexterityscore] = useState(1)
    const [responseData, setResponseData] = useState('')
    const [variant, setVariant] = useState('')
    const [show, setShow] = useState(false)

    const { register, watch, handleSubmit, reset, formState: { errors } } = useForm()

    const signupSubmitForm = (data) => {
        console.log("Sign-Up form submitted with below details.")
        const formData = {
            gender: gender,
            illness: illness,
            mobilityscore: mobilityscore,
            dexterityscore: dexterityscore
        }
        console.log({ ...data, ...formData })

        if (data.password === data.confirmPassword) {
            const body = JSON.stringify({ ...data, ...formData })
            const headers = {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            }

            axios.post('/user/signup', body, { headers: headers })
                .then(response => {
                    console.log("Success from fetching from signup endpoint.")
                    console.log(response.data)
                    setResponseData(response.data)
                    setShow(true)
                    setVariant("success")
                })
                .catch(error => {
                    console.log("Error occured from fetching from signup endpoint")
                    console.log(error.response.data)
                    setResponseData(error.response.data)
                    setShow(true)
                    setVariant("danger")
                })

            reset()
        }
        else {
            alert("Passwords dont match. Please try again.")
        }
    }

    console.log(watch("username"))

    return (
        <section class="h-100 h-custom" style={{ backgroundColor: '#F8EEE3' }}>
            <div class="mask d-flex align-items-center h-100">
                <div className="container h-100">
                    <div class="row d-flex justify-content-center align-items-center h-100">
                        <div class="col-lg-8 col-xl-6">
                            <div class="signup-card rounded-3" style={{ backgroundColor: 'white' }}>
                                <img src={signupImage} class="w-100" style={{ borderTopLeftRadius: 10, borderTopRightRadius: 10 }} />
                                <div class="card-body p-4 p-md-5">
                                    <h1 class="text-uppercase text-center mb-5" style={{ fontWeight: 'bold' }}>Create an account </h1>
                                    <form>
                                        <Form.Group>
                                            <Form.Label style={{ fontSize: "20px" }}>Username</Form.Label>
                                            <Form.Control type="text"
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
                                            <Form.Label style={{ fontSize: "20px" }}>Email</Form.Label>
                                            <Form.Control type="email"
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
                                            <Form.Label style={{ fontSize: "20px" }}>Password</Form.Label>
                                            <Form.Control type="password"
                                                {...register("password", { required: true, minLength: 6, maxLength: 18 })}
                                            />
                                            {errors.password?.type === "required" && <span style={{ color: "red", fontSize: 14 }}>password is required</span>}
                                            {errors.password?.type === "minLength" && <span style={{ color: "red", fontSize: 14 }}>password should have minimum of 6 characters</span>}
                                            {errors.password?.type === "maxLength" && <span style={{ color: "red", fontSize: 14 }}>password cannot exceed 18 characters</span>}
                                        </Form.Group>
                                        <br></br>
                                        <Form.Group>
                                            <Form.Label style={{ fontSize: "20px" }}>Confirm password</Form.Label>
                                            <Form.Control type="password" placeholder="Repeat your password"
                                                {...register("confirmPassword", { required: true, minLength: 6, maxLength: 18 })}
                                            />
                                            {errors.confirmPassword?.type === "required" && <span style={{ color: "red", fontSize: 14 }}>confirm password field is required</span>}
                                            {errors.confirmPassword?.type === "minLength" && <span style={{ color: "red", fontSize: 14 }}>confirm password should have minimum of 6 characters</span>}
                                            {errors.confirmPassword?.type === "maxLength" && <span style={{ color: "red", fontSize: 14 }}>confirm password cannot exceed 18 characters</span>}
                                        </Form.Group>
                                        <br></br>
                                        <Form.Group>
                                            <Form.Label style={{ fontSize: "20px" }}>First Name</Form.Label>
                                            <Form.Control type="text"
                                                {...register("firstname", { required: true, minLength: 3, maxLength: 50 })}
                                            />
                                            {errors.firstname?.type === "required" && <span style={{ color: "red", fontSize: 14 }}>firstname is required</span>}
                                            {errors.firstname?.type === "minLength" && <span style={{ color: "red", fontSize: 14 }}>firstname should have minimum of 3 characters</span>}
                                            {errors.firstname?.type === "maxLength" && <span style={{ color: "red", fontSize: 14 }}>firstname cannot exceed 50 characters</span>}
                                        </Form.Group>
                                        <br></br>
                                        <Form.Group>
                                            <Form.Label style={{ fontSize: "20px" }}>Last Name</Form.Label>
                                            <Form.Control type="text"
                                                {...register("lastname", { required: true, minLength: 3, maxLength: 50 })}
                                            />
                                            {errors.lastname?.type === "required" && <span style={{ color: "red", fontSize: 14 }}>lastname is required</span>}
                                            {errors.lastname?.type === "minLength" && <span style={{ color: "red", fontSize: 14 }}>lastname should have minimum of 3 characters</span>}
                                            {errors.lastname?.type === "maxLength" && <span style={{ color: "red", fontSize: 14 }}>lastname cannot exceed 50 characters</span>}
                                        </Form.Group>
                                        <br></br>
                                        <Form.Group>
                                            <Form.Label style={{ fontSize: "20px" }}>Age (in years)</Form.Label>
                                            <Form.Control type="number" min='1' max='150'
                                                {...register("age", { required: true, valueAsNumber: true })}
                                            />
                                            {errors.age?.type === "required" && <span style={{ color: "red", fontSize: 14 }}>age is required</span>}
                                        </Form.Group>
                                        <br></br>
                                        <Form.Group controlId="formBasicSelect1">
                                            <Form.Label style={{ fontSize: "20px" }}>Gender</Form.Label>
                                            <div className="mb-3">
                                                <Form.Check inline value="Male" label="Male" name="gender" type='radio' onChange={(event) => { setGender(event.target.value) }} />
                                                <Form.Check inline value="Female" label="Female" name="gender" type='radio' onChange={(event) => { setGender(event.target.value) }} />
                                            </div>
                                        </Form.Group>
                                        <br></br>
                                        <Form.Group>
                                            <Form.Label style={{ fontSize: "20px" }}>Height (in cm)</Form.Label>
                                            <Form.Control type="number"
                                                min='1'
                                                {...register("height", { required: true, valueAsNumber: true })}
                                            />
                                            {errors.height?.type === "required" && <span style={{ color: "red", fontSize: 14 }}>height is required</span>}
                                        </Form.Group>
                                        <br></br>
                                        <Form.Group>
                                            <Form.Label style={{ fontSize: "20px" }}>Weight (in kg)</Form.Label>
                                            <Form.Control type="number"
                                                min='1'
                                                {...register("weight", { required: true, valueAsNumber: true })}
                                            />
                                            {errors.weight?.type === "required" && <span style={{ color: "red", fontSize: 14 }}>weight is required</span>}
                                        </Form.Group>
                                        <br></br>
                                        <Form.Group controlId="formBasicSelect2">
                                            <Form.Label style={{ fontSize: "20px" }}>Medical background</Form.Label>
                                            <Form.Control as="select"
                                                value={illness}
                                                name="illness"
                                                onChange={(event) => { setIllness(event.target.value) }}>
                                                <option>Select, if any (else select 'No').</option>
                                                <option value={"Hypertension"}>Hypertension</option>
                                                <option value={"Cholesterol"}>Cholesterol</option>
                                                <option value={"Diabetes"}>Diabetes</option>
                                                <option value={"Coronary Heart Disease"}>Coronary Heart Disease</option>
                                                <option value={"Arthritis"}>Arthritis</option>
                                                <option value={"Ulcer"}>Ulcer</option>
                                                <option value={"No"}>No</option>
                                            </Form.Control>
                                        </Form.Group>
                                        <br></br>
                                        <Form.Group>
                                            <Form.Label style={{ fontSize: "20px" }}>Mobility Score</Form.Label>
                                            <p>(20 - excellent mobility, 1 - requires assistance)</p>
                                            <RangeSlider
                                                variant='primary'
                                                value={mobilityscore}
                                                onChange={(event) => { setMobilityscore(event.target.value) }}
                                                tooltip='on'
                                                min={1}
                                                max={20} />
                                        </Form.Group>
                                        <br></br>
                                        <br></br>
                                        <Form.Group>
                                            <Form.Label style={{ fontSize: "20px" }}>Dexterity Score</Form.Label>
                                            <p>(3 - excellent controlled hand and finger movements, 1 - requires assistance)</p>
                                            <RangeSlider
                                                variant='success'
                                                value={dexterityscore}
                                                onChange={(event) => { setDexterityscore(event.target.value) }}
                                                tooltip='on'
                                                min={1}
                                                max={3} />
                                        </Form.Group>
                                        <br></br>
                                        {show ?
                                            <>
                                                <Alert key={variant} variant={variant} onClose={() => { setShow(false) }} dismissible>
                                                    <p>{responseData.message}</p>
                                                    {variant === "success" &&
                                                        <p>Login <Link to='/login'>now</Link> to get started on your journey.</p>
                                                    }
                                                </Alert>
                                            </>
                                            : <br></br>
                                        }
                                        <Form.Group>
                                            <div class="d-flex justify-content-center">
                                                <Button variant="primary" class="btn btn-primary btn-block btn-lg" onClick={handleSubmit(signupSubmitForm)}>
                                                    SIGN-UP
                                                </Button>
                                            </div>
                                        </Form.Group>
                                        <br></br>
                                        <br></br>
                                        <Form.Group>
                                            <small>
                                                Existing user? Login <Link to='/login' style={{ fontWeight: 'bold' }}>here</Link> to pick up where you left off and view your tailored recommendations.
                                            </small>
                                        </Form.Group>
                                    </form>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </section >
    )
}

export default SignupPage