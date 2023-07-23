import React, { useEffect, useState } from 'react'
import { Form, Button, Modal } from 'react-bootstrap'
import { useNavigate } from 'react-router-dom'
import { useForm } from 'react-hook-form'
import axios from 'axios'
import { logout } from '../Auth'
import UserProfile from './UserProfile'
import '../css/MyAccount.css'

const MyAccountPage = () => {
    const [gender, setGender] = useState('')
    const [illness, setIllness] = useState('')
    const [userProfile, setUserProfile] = useState('')
    const [show, setShow] = useState('')
    const { register, watch, handleSubmit, reset, setValue, formState: { errors } } = useForm()
    const navigate = useNavigate()

    let accessToken = localStorage.getItem('REACT_TOKEN_AUTH_KEY')
    let userId = localStorage.getItem('id')

    const closeModal = () => {
        setShow(false)
    }

    const showModal = (id) => {
        console.log('Update button pressed.')
        console.log(id)
        setValue('firstname', userProfile.Firstname)
        setValue('lastname', userProfile.Lastname)
        setValue('age', userProfile.Age)
        setValue('height', userProfile.Height)
        setValue('weight', userProfile.Weight)
        setShow(true)
    }

    const deleteUser = (id) => {
        console.log('Delete button pressed.')
        console.log(id)

        const headers = {
            'Authorization': `Bearer ${JSON.parse(accessToken)}`
        }
        axios.delete(`/user/${userId}`, { headers: headers })
            .then(response => {
                console.log("Success deleting the user profile.")
                console.log(response.data)

                // logout & redirect to end user page
                logout()
                navigate('/enduser')
            }).catch(error => {
                console.log("Error occured while deleting user profile.")
                console.log(error.response)
            })

    }

    const updateUser = (data) => {
        console.log('Updated user profile details submitted.')
        const formData = {
            gender: gender,
            illness: illness
        }
        console.log({ ...data, ...formData })
        const headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${JSON.parse(accessToken)}`
        }
        const body = JSON.stringify({ ...data, ...formData })

        axios.put(`/user/${userId}`, body, { headers: headers })
            .then(response => {
                console.log("Success updating the user profile.")
                console.log(response.data)
                setUserProfile(response.data)
                // reload the page after the details are updated
                const reload = window.location.reload()
                reload()
            }).catch(error => {
                console.log("Error occured while updating user profile.")
                console.log(error.response)
            })
    }

    const headers = {
        'Authorization': `Bearer ${JSON.parse(accessToken)}`
    }
    useEffect(() => {
        axios.get(`/user/${userId}`, { headers: headers })
            .then(response => {
                console.log("Success fetching the user profile.")
                console.log(response.data)
                setUserProfile(response.data)
            }).catch(error => {
                console.log("Error occured while fetching user profile.")
                console.log(error.response)
            })
    }, [])

    return (
        <>
            <Modal show={show} size="lg" onHide={closeModal}>
                <Modal.Header closeButton>
                    <Modal.Title>
                        UPDATE YOUR DETAILS HERE
                    </Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    <form>
                        <Form.Group>
                            <Form.Label style={{ fontSize: "20px" }}>Username</Form.Label>
                            <Form.Control type="text" placeholder={userProfile.Username} disabled readOnly />
                            <span style={{ color: "green", fontSize: 14 }}>username cannot be modified</span>
                        </Form.Group>
                        <br></br>
                        <Form.Group>
                            <Form.Label style={{ fontSize: "20px" }}>Email</Form.Label>
                            <Form.Control type="email" placeholder={userProfile.Email} disabled readOnly />
                            <span style={{ color: "green", fontSize: 14 }}>email address cannot be modified</span>
                        </Form.Group>
                        <br></br>
                        <Form.Group>
                            <Form.Label style={{ fontSize: "20px" }}>First Name</Form.Label>
                            <Form.Control type="text"
                                {...register("firstname", { minLength: 3, maxLength: 50 })}
                            />
                            {errors.firstname?.type === "minLength" && <span style={{ color: "red", fontSize: 14 }}>firstname should have minimum of 3 characters</span>}
                            {errors.firstname?.type === "maxLength" && <span style={{ color: "red", fontSize: 14 }}>firstname cannot exceed 50 characters</span>}
                        </Form.Group>
                        <br></br>
                        <Form.Group>
                            <Form.Label style={{ fontSize: "20px" }}>Last Name</Form.Label>
                            <Form.Control type="text"
                                {...register("lastname", { minLength: 3, maxLength: 50 })}
                            />
                            {errors.lastname?.type === "minLength" && <span style={{ color: "red", fontSize: 14 }}>lastname should have minimum of 3 characters</span>}
                            {errors.lastname?.type === "maxLength" && <span style={{ color: "red", fontSize: 14 }}>lastname cannot exceed 50 characters</span>}
                        </Form.Group>
                        <br></br>
                        <Form.Group>
                            <Form.Label style={{ fontSize: "20px" }}>Age (years)</Form.Label>
                            <Form.Control type="number" min='1' max='150'
                                {...register("age", { valueAsNumber: true })}
                            />
                        </Form.Group>
                        <br></br>
                        <Form.Group>
                            <Form.Label style={{ fontSize: "20px" }}>Height (cm)</Form.Label>
                            <Form.Control type="number"
                                min='1'
                                {...register("height", { valueAsNumber: true })}
                            />
                        </Form.Group>
                        <br></br>
                        <Form.Group>
                            <Form.Label style={{ fontSize: "20px" }}>Weight (kg)</Form.Label>
                            <Form.Control type="number"
                                min='1'
                                {...register("weight", { valueAsNumber: true })}
                            />
                        </Form.Group>
                        <br></br>
                        <Form.Group controlId="formBasicSelect2">
                            <Form.Label style={{ fontSize: "20px" }}>Medical background</Form.Label>
                            <Form.Control as="select"
                                value={illness}
                                name="illness"
                                onChange={(event) => { setIllness(event.target.value) }}>
                                <option value={"Hypertension"}>Hypertension</option>
                                <option value={"Cholesterol"}>Cholesterol</option>
                                <option value={"Diabetes"}>Diabetes</option>
                                <option value={"Coronary Heart Disease"}>Coronary Heart Disease</option>
                                <option value={"Arthritis"}>Arthritis</option>
                                <option value={"No"}>No</option>
                            </Form.Control>
                        </Form.Group>
                        <Form.Group>
                            <div className="d-flex justify-content-center">
                                <Button as="sub" variant="primary" class="btn btn-primary btn-block btn-lg" onClick={handleSubmit(updateUser)}>Save</Button>
                            </div>
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
                onDelete={() => { deleteUser(userProfile.id) }}
            />

        </>
    )
}

export default MyAccountPage