import React, { useEffect, useState } from 'react'
import { Form, Button, Modal } from 'react-bootstrap'
import { useNavigate } from 'react-router-dom'
import { useForm } from 'react-hook-form'
import axios from 'axios'
import { logout } from '../Auth'
import FoodCard from './FoodCard'

const RecipeRecommendationPage = () => {
    const [recommendedFoodProfiles, setRecommendedFoodProfiles] = useState('')
    const [similarFoodProfiles, setSimilarFoodProfiles] = useState('')
    const [similarUserFoodProfiles, setSimilarUserFoodProfiles] = useState([])

    let userId = localStorage.getItem('id')

    // Get recipe from flask endpoint
    useEffect(() => {
        axios.get(`/recommend/${userId}/foods`)
            .then(response => {
                console.log("Success fetching the food recommendations.")
                console.log(response.data)
                setRecommendedFoodProfiles(response.data.recommended_foods)
                setSimilarFoodProfiles(response.data.similar_food_choices)
                setSimilarUserFoodProfiles(response.data.similar_user_food_choices)
            }).catch(error => {
                console.log("Error occured while fetching the recommended foods.")
                console.log(error.response)
            })
    }, [])



    return (

        <div className='container'>
            <h1>Hi this is where you will see your list of recommeded recipes</h1>
            <div className='recommended recipes'>
                <h4>Recommended recipes</h4>
                {
                    Object.keys(recommendedFoodProfiles).map((mealType) => (
                        <div key={mealType}>
                            <h5>{mealType}</h5>
                            {recommendedFoodProfiles[mealType].map((recipes) => (
                                <div key={recipes.id}>
                                <FoodCard
                                    Name={recipes.Name}
                                    Quantity={recipes.Quantity}
                                    Calories={recipes.Calories}
                                />
                                </div>
                            ))}
                        </div>
                    ))}
            </div>
            <div className='similar food recipes '>
                <h4>Foods similar to recommendations from above</h4>
                {
                    Object.keys(similarFoodProfiles).map((mealType) => (
                        <div key={mealType}>
                            <h5>{mealType}</h5>
                            {similarFoodProfiles[mealType].map((recipes) => (
                                <div key={recipes.id}>
                                    <FoodCard
                                        Name={recipes.Name}
                                        Calories={recipes.Calories}
                                    />
                                </div>
                            ))}
                        </div>
                    ))}
            </div>
            <div className='similar user food recipes '>
                <h4>Foods liked by users similar to you</h4>
                {
                    similarUserFoodProfiles.map((recipes) => (
                        <div key={recipes.id}>
                            <FoodCard
                                Name={recipes.Name}
                                Calories={recipes.Calories}
                            />
                        </div>
                    ))}
            </div>
        </div >
    )
}

export default RecipeRecommendationPage