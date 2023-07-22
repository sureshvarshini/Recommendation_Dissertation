import React from 'react'
import { Card, Modal, Button } from 'react-bootstrap'

const FoodCard = ({ Name, Quantity, Calories }) => {

    return (
        <div>
            <Card className='food profile'>
                <Card.Body>
                    <Card.Title>{Name}</Card.Title>
                    <p>Quantity : {Quantity}</p>
                    <p>Calories : {Calories}</p>
                </Card.Body>
            </Card>
        </div>
    )
}

export default FoodCard