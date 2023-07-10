import React, { useEffect, useState } from 'react'
import { Form, Button, Modal } from 'react-bootstrap'
import { useForm } from 'react-hook-form'
import axios from 'axios'
import UserProfile from './UserProfile'

const MyAccountPage = () => {
    const [gender, setGender] = useState('')
    const [illness, setIllness] = useState('')
    const [userProfile, setUserProfile] = useState('')
    const [show, setShow] = useState('')
    const { register, watch, handleSubmit, reset, formState: { errors } } = useForm()

    const closeModal = () => {
        setShow(false)
    }

    const showModal = (id) => {
        setShow(true)
    }

    const updateUser = (data) => {
        const formData = {
            gender: gender,
            illness: illness
        }
        console.log({ ...data, ...formData })
    }

    const accessToken = localStorage.getItem('REACT_TOKEN_AUTH_KEY')
    const headers = {
        'Authorization': `Bearer ${JSON.parse(accessToken)}`
    }
    useEffect(() => {
        axios.get('/user/5', { headers: headers })
            .then(response => {
                console.log("Success fetching the user profile.")
                console.log(response.data)
                setUserProfile(response.data)
                console.log('user id')
            }).catch(error => {
                console.log("Error occured while fetching user profile.")
                console.log(error.response)
                console.log(`Bearer ${JSON.parse(accessToken)}`)
            })
    }, [])

    return (
        <>
            <h1>My Account</h1>
            <Modal show={show} size="lg" onHide={closeModal}>
                <Modal.Header closeButton>
                    <Modal.Title>
                        Update user details.
                    </Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    <form>
                        <Form.Group>
                            <Form.Label>Username</Form.Label>
                            <Form.Control type="text" placeholder={userProfile.Username} disabled readOnly/>
                            <span style={{ color: "red", fontSize: 14 }}>username cannot be modified</span>
                        </Form.Group>
                        <br></br>
                        <Form.Group>
                            <Form.Label>Email</Form.Label>
                            <Form.Control type="email" placeholder="Your email address here."
                                {...register("email", {
                                    validate: {
                                        matchPattern: (v) =>
                                            /^\w+([.-]?\w+)*@\w+([.-]?\w+)*(\.\w{2,3})+$/.test(v)
                                    }
                                })}
                            />
                            {errors.email?.type === "matchPattern" && <span style={{ color: "red", fontSize: 14 }}>email address should be valid</span>}
                        </Form.Group>
                        <br></br>
                        <Form.Group>
                            <Form.Label>First Name</Form.Label>
                            <Form.Control type="text" placeholder="Your first name here."
                                {...register("firstname", { minLength: 3, maxLength: 50 })}
                            />
                            {errors.firstname?.type === "minLength" && <span style={{ color: "red", fontSize: 14 }}>firstname should have minimum of 3 characters</span>}
                            {errors.firstname?.type === "maxLength" && <span style={{ color: "red", fontSize: 14 }}>firstname cannot exceed 50 characters</span>}
                        </Form.Group>
                        <br></br>
                        <Form.Group>
                            <Form.Label>Last Name</Form.Label>
                            <Form.Control type="text" placeholder="Your last name here."
                                {...register("lastname", { minLength: 3, maxLength: 50 })}
                            />
                            {errors.lastname?.type === "minLength" && <span style={{ color: "red", fontSize: 14 }}>lastname should have minimum of 3 characters</span>}
                            {errors.lastname?.type === "maxLength" && <span style={{ color: "red", fontSize: 14 }}>lastname cannot exceed 50 characters</span>}
                        </Form.Group>
                        <br></br>
                        <Form.Group>
                            <Form.Label>Age</Form.Label>
                            <Form.Control type="number" placeholder="Your age here." min='1' max='150'
                                {...register("age", { valueAsNumber: true })}
                            />
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
                                {...register("height", { valueAsNumber: true })}
                            />
                        </Form.Group>
                        <br></br>
                        <Form.Group>
                            <Form.Label>Weight</Form.Label>
                            <Form.Control type="number"
                                min='1'
                                placeholder="Your weight here (in kg)."
                                {...register("weight", { valueAsNumber: true })}
                            />
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
                        <Form.Group>
                            <Button as="sub" variant="primary" onClick={handleSubmit(updateUser)}>
                                Save
                            </Button>
                        </Form.Group>
                        <br></br>
                    </form>
                </Modal.Body>
            </Modal>

            <UserProfile
                Username={userProfile.Username}
                Firstname={userProfile.Firstname}
                Lastname={userProfile.Lastname}
                Email={userProfile.Email}
                Gender={userProfile.Gender}
                Age={userProfile.Age}
                Height={userProfile.Height}
                Weight={userProfile.Weight}
                Illness={userProfile.Illness}
                onClick={() => { showModal(userProfile.id) }}
            />
        </>
    )
}

export default MyAccountPage