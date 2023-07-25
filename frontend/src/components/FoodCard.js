import React from 'react'
import { Card, Modal, Button } from 'react-bootstrap'
import foodPlaceholder from "../assets/food_placeholder.jpg"
import '../css/FoodCard.css'

const FoodCard = ({ Name, Quantity, Calories, Servings, Ingredients, Directions, onClick }) => {

    return (
        <div className='card' onClick={onClick}>
            <div className='card-header'>
                <div className='card-title-group'>
                    <h5 className="card-title">{Name}</h5>
                </div>
            </div>
            <img className='card-image' src={foodPlaceholder} alt='Logo' />
            <div className='card-text fst-italic'><span style={{ fontWeight: 'bold' }}>Calories: </span>{Calories}</div>
        </div>
    )
}

export default FoodCard