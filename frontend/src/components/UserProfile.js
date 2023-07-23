import React from 'react'
import { Card, Modal, Button } from 'react-bootstrap'
import femaleProfilePicture from "../assets/female_profile_placeholder.jpg"
import maleProfilePicture from "../assets/male_profile_placeholder.jpg"

const UserProfile = ({ Username, Firstname, Lastname, Email, Gender, Age, Height, Weight, Illness, onClick, onDelete }) => {
    return (
        <section className="vh-100" style={{ backgroundColor: '#f4f5f7' }}>
            <div className="container h-100">
                <div className="row d-flex justify-content-center align-items-center h-100">
                    <div className="col col-lg-6 mb-4 mb-lg-0">
                        <div className="my-account-card mb-3" style={{ borderRadius: 20, backgroundColor: 'white', width: '900px' }}>
                            <div className="row g-0">
                                <div className="col-md-4 gradient-custom text-center text-white"
                                    style={{ borderTopLeftRadius: 10, borderBottomLeftRadius: 10 }}>
                                    <img src={Gender == "Male" ? maleProfilePicture : femaleProfilePicture} className="img-fluid my-5" style={{ width: '300px' }} />
                                    <h3>{Firstname} </h3>
                                    <h3>{Lastname}</h3>
                                    <p style={{ fontStyle: 'italic' }}>{Username}</p>
                                    <div className="d-flex justify-content-center">
                                        <Button variant='dark' size="lg" style={{ width: '100%', fontWeight: 'bold'}} onClick={onClick}>Update Account</Button>
                                    </div>
                                </div>
                                <div className="col-md-7">
                                    <div className="my-account-card-body p-4">
                                        <h3>My Information</h3>
                                        <hr className="mt-0 mb-3" />
                                        <div className="row pt-1">
                                            <div className="col-5 mb-3">
                                                <h5>Email</h5>
                                                <p className="text-muted" style={{ fontSize: '14px' }}>{Email}</p>
                                            </div>
                                            <div className="col-4 mb-3">
                                                <h5>Gender</h5>
                                                <p className="text-muted" style={{ fontSize: '16px' }}>{Gender}</p>
                                            </div>
                                            <div className="col-3 mb-3">
                                                <h5>Age</h5>
                                                <p className="text-muted" style={{ fontSize: '16px' }}>{Age}</p>
                                            </div>
                                        </div>
                                        <h4>Body Vitals</h4>
                                        <hr className="mt-0 mb-4"></hr>
                                        <div className="row pt-1">
                                            <div className="col-5 mb-3">
                                                <h5>Height (cm)</h5>
                                                <p className="text-muted" style={{ fontSize: '16px' }}>{Height}</p>
                                            </div>
                                            <div className="col-4 mb-3">
                                                <h5>Weight (kg)</h5>
                                                <p className="text-muted" style={{ fontSize: '16px' }}>{Weight}</p>
                                            </div>
                                        </div>
                                        <h4>Medical Background</h4>
                                        <hr className="mt-0 mb-4"></hr>
                                        <div className="row pt-1">
                                            <div className="col-4 mb-3">
                                                <p className="text-muted" style={{ fontSize: '19px' }}>{Illness}</p>
                                            </div>

                                        </div>
                                    </div>
                                    <div className="d-flex justify-content-end">
                                        <Button variant='danger' size="lg" onClick={onDelete}>Delete Account</Button>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </section >
    )
}

export default UserProfile