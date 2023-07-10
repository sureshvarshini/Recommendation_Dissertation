import React from 'react'
import { Card, Modal, Button } from 'react-bootstrap'

const UserProfile = ({ Username, Firstname, Lastname, Email, Gender, Age, Height, Weight, Illness, onClick }) => {
    return (
        <Card className='user profile'>
            <Card.Body>
                <h5>Username: {Username}</h5>
                <h5>Firstname: {Firstname}</h5>
                <h5>Lastname: {Lastname}</h5>
                <h5>Email: {Email}</h5>
                <h5>Gender: {Gender}</h5>
                <h5>Age: {Age}</h5>
                <h5>Height: {Height}</h5>
                <h5>Weight: {Weight}</h5>
                <h5>Illness: {Illness}</h5>
                <Button variant='primary' onClick={onClick}>Update</Button>
            </Card.Body>
        </Card>
    )
}

export default UserProfile