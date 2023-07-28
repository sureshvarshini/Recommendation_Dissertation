import React from 'react'
import foodPlaceholder from "../assets/food_placeholder.jpg"
import '../css/FoodCard.css'

const FoodCard = ({ Name, Calories, Image, onClick }) => {

    return (
        <div className='food-card' onClick={onClick}>
            <div className='food-card-header'>
                <div className='food-card-title-group'>
                    <h5 className='food-card-title'>{Name}</h5>
                </div>
            </div>
            <img className='food-card-image' src={Image === "https://myplate-prod.azureedge.us/sites/default/files/styles/medium/public/default_images/mpk-default-1000.png?itok=MHDkRduG" ? foodPlaceholder : Image} alt={Name} />
            <div className='food-card-text fst-italic' style={{ fontSize: 'x-large' }}><span style={{ fontWeight: 'bold' }}>Calories: </span>{Calories}</div>
        </div>
    )
}

export default FoodCard