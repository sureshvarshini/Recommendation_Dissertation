import React, { useEffect, useState } from 'react'
import { Form, Button, Modal } from 'react-bootstrap'
import { useNavigate } from 'react-router-dom'
import { useForm } from 'react-hook-form'
import Slider from 'react-slick';
import axios from 'axios'
import FoodCard from './FoodCard'
import 'slick-carousel/slick/slick.css';
import 'slick-carousel/slick/slick-theme.css';

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

    const settings = {
        dots: true,
        infinite: true,
        slidesToShow: 2,
        slidesToScroll: 1,
        nextArrow: (
            <div>
                <div className="next-slick-arrow"> ⫸ </div>
            </div>
        ),
        prevArrow: (
            <div>
                <div className="prev-slick-arrow"> ⫷ </div>
            </div>
        )
    };


    return (
        <div className='container'>
            <div class="d-flex justify-content-center">
                <h3 style={{ fontWeight: 'bold', marginTop: '20px', textAlign: "center" }}>Greetings!! Your list of recommended recipes awaits you on this page.</h3>
            </div>
            <div class="d-flex">
                <h3 style={{ fontWeight: 'bold', marginTop: '20px' }}>Curated selections just for you.</h3>
            </div>
            <div className='recommended recipes'>
                {Object.keys(recommendedFoodProfiles).map((mealType) => (
                    <div key={mealType}>
                        <h2 style={{ display: 'flex', justifyContent: 'center', color: 'white', marginTop: '30px', backgroundColor: '#FF0078', borderRadius: '10px', padding: 10 }}>{mealType}</h2>
                        <Slider {...settings}>
                            {recommendedFoodProfiles[mealType].map((recipes) => (
                                <div key={recipes.id}>
                                    <FoodCard
                                        Name={recipes.Name}
                                        Quantity={recipes.Quantity}
                                        Calories={recipes.Calories}
                                    />
                                </div>
                            ))}
                        </Slider>
                    </div>
                ))}
            </div>

            <div className='similar food recipes '>
                <h3 style={{ fontWeight: 'bold', marginTop: '40px' }}>Similar food choices to the above suggestions.</h3>
                {Object.keys(similarFoodProfiles).map((mealType) => (
                    <div key={mealType}>
                        <h2 style={{ display: 'flex', justifyContent: 'center', color: 'white', marginTop: '30px', backgroundColor: '#029922', borderRadius: '10px', padding: 10 }}>{mealType}</h2>
                        <Slider {...settings}>
                            {similarFoodProfiles[mealType].map((recipes) => (
                                <div key={recipes.id}>
                                    <FoodCard
                                        Name={recipes.Name}
                                        Calories={recipes.Calories}
                                    />
                                </div>
                            ))}
                        </Slider>
                    </div>
                ))}
            </div>
            <div className='similar user food recipes '>
                <h3 style={{ fontWeight: 'bold', marginTop: '40px' }}>Foods preferred by individuals similar to your taste.</h3>
                <Slider {...settings}>
                    {similarUserFoodProfiles.map((recipes) => (
                        <div key={recipes.id}>
                            <FoodCard
                                Name={recipes.Name}
                                Calories={recipes.Calories}
                            />
                        </div>
                    ))}
                </Slider>
            </div>
        </div >
    )
}

export default RecipeRecommendationPage