import React, { useEffect, useState } from 'react'
import { Modal } from 'react-bootstrap'
import Slider from 'react-slick';
import axios from 'axios'
import FoodCard from './FoodCard'
import 'slick-carousel/slick/slick.css';
import 'slick-carousel/slick/slick-theme.css';

const RecipeRecommendationPage = () => {
    const [recommendedFoodProfiles, setRecommendedFoodProfiles] = useState('')
    const [done, setDone] = useState(undefined)
    const [similarFoodProfiles, setSimilarFoodProfiles] = useState('')
    const [similarUserFoodProfiles, setSimilarUserFoodProfiles] = useState([])
    const [selectedFoodProfile, setSelectedFoodProfile] = useState([])
    const [ingredientsList, setIngredientsList] = useState([])
    const [directionsList, setDirectionsList] = useState([])
    const [show, setShow] = useState('')

    let userId = localStorage.getItem('id')

    const closeModal = () => {
        setShow(false)
    }

    const showModal = (recipe) => {
        console.log('Recipe card clicked.')
        console.log(recipe)
        setSelectedFoodProfile(recipe)
        setIngredientsList((recipe.Ingredients).split(','))
        setDirectionsList((recipe.Directions).split('.,'))
        console.log(directionsList)
        setShow(true)
    }

    // Get recipe from flask endpoint
    useEffect(() => {
        axios.get(`/recommend/${userId}/foods`)
            .then(response => {
                console.log("Success fetching the food recommendations.")
                console.log(response.data)
                setRecommendedFoodProfiles(response.data.recommended_foods)
                setSimilarFoodProfiles(response.data.similar_food_choices)
                setSimilarUserFoodProfiles(response.data.similar_user_food_choices)
                console.log(similarUserFoodProfiles)
                setDone(true)
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
            <Modal show={show} size="lg" onHide={closeModal} style={{ padding: 150 }}>
                <Modal.Header closeButton>
                    <Modal.Title style={{ fontWeight: 'bold' }}>
                        {selectedFoodProfile?.Name}
                    </Modal.Title>
                </Modal.Header>
                <Modal.Body style={{ fontSize: '20px' }}>
                    <p style={{ fontWeight: 'bold' }}>Ingredients:</p>
                    <ul>
                        {ingredientsList.map((i, index) => (
                            <li key={index}>{i}</li>
                        ))}
                    </ul>
                    <p style={{ fontWeight: 'bold' }}>Directions:</p>
                    <ul>
                        {directionsList.map((i, index) => (
                            <li key={index}>{i}</li>
                        ))}
                    </ul>
                </Modal.Body>
            </Modal>
            <div class="d-flex justify-content-center">
                <h3 style={{ fontWeight: 'bold', marginTop: '20px', textAlign: "center" }}>Greetings!! Your list of recommended recipes awaits you on this page.</h3>
            </div>
            <div class="d-flex">
                <h3 style={{ fontWeight: 'bold', marginTop: '20px' }}>Curated selections just for you.</h3>
            </div>
            {!done ? (
                <div class="d-flex justify-content-left">
                    <small>Loading....</small>
                    <div class="spinner-grow spinner-grow-sm text-primary" role="status">
                        <span class="sr-only"></span>
                    </div>
                    <div class="spinner-grow spinner-grow-sm text-secondary" role="status">
                        <span class="sr-only"></span>
                    </div>
                    <div class="spinner-grow spinner-grow-sm text-success" role="status">
                        <span class="sr-only"></span>
                    </div>
                    <div class="spinner-grow spinner-grow-sm text-danger" role="status">
                        <span class="sr-only"></span>
                    </div>
                    <div class="spinner-grow spinner-grow-sm text-warning" role="status">
                        <span class="sr-only"></span>
                    </div>
                    <div class="spinner-grow spinner-grow-sm text-info" role="status">
                        <span class="sr-only"></span>
                    </div>
                    <div class="spinner-grow spinner-grow-sm text-light" role="status">
                        <span class="sr-only"></span>
                    </div>
                </div>
            ) : (
                <div className='recommended recipes'>
                    {Object.keys(recommendedFoodProfiles).map((mealType) => (
                        <div key={mealType}>
                            <h2 style={{ display: 'flex', justifyContent: 'center', color: 'white', marginTop: '30px', backgroundColor: '#FF0078', borderRadius: '10px', padding: 10 }}>{mealType}</h2>
                            <Slider {...settings}>
                                {recommendedFoodProfiles[mealType].map((recipe) => (
                                    <div key={recipe.id}>
                                        <FoodCard
                                            Name={recipe.Name}
                                            Quantity={recipe.Quantity}
                                            Calories={recipe.Calories}
                                            Servings={recipe.Servings}
                                            Directions={recipe.Directions}
                                            Ingredients={recipe.Ingredients}
                                            onClick={() => { showModal(recipe) }}
                                        />
                                    </div>
                                ))}
                            </Slider>
                        </div>
                    ))}
                </div>
            )}
            {/* <div className='similar food recipes '>
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
            </div> */}
            <div className='similar user food recipes '>
                <h3 style={{ fontWeight: 'bold', marginTop: '40px' }}>Foods preferred by individuals similar to your taste.</h3>
                {!done ? (
                    <div class="d-flex justify-content-left">
                        <small>Loading....</small>
                        <div class="spinner-grow spinner-grow-sm text-primary" role="status">
                            <span class="sr-only"></span>
                        </div>
                        <div class="spinner-grow spinner-grow-sm text-secondary" role="status">
                            <span class="sr-only"></span>
                        </div>
                        <div class="spinner-grow spinner-grow-sm text-success" role="status">
                            <span class="sr-only"></span>
                        </div>
                        <div class="spinner-grow spinner-grow-sm text-danger" role="status">
                            <span class="sr-only"></span>
                        </div>
                        <div class="spinner-grow spinner-grow-sm text-warning" role="status">
                            <span class="sr-only"></span>
                        </div>
                        <div class="spinner-grow spinner-grow-sm text-info" role="status">
                            <span class="sr-only"></span>
                        </div>
                        <div class="spinner-grow spinner-grow-sm text-light" role="status">
                            <span class="sr-only"></span>
                        </div>
                    </div>
                ) : (
                    <Slider {...settings}>
                        {similarUserFoodProfiles.map((recipe) => (
                            <div key={recipe.id}>
                                <FoodCard
                                    Name={recipe.Name}
                                    Calories={recipe.Calorie}
                                    Servings={recipe.Servings}
                                    Directions={recipe.Directions}
                                    Ingredients={recipe.Ingredients}
                                    onClick={() => { showModal(recipe) }}
                                />
                            </div>
                        ))}
                    </Slider>)}
            </div>
        </div >
    )
}

export default RecipeRecommendationPage