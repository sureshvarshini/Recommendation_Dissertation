import React from 'react'
import Walking from '../assets/Walking.jpg'
import Jogging from '../assets/Jogging.jpg'
import ModelBuilding from '../assets/model_building.jpg'
import Origami from '../assets/origami.jpg'
import Gardening from '../assets/Gardening.jpg'
import Yoga from '../assets/Yoga.jpg'
import Reading from '../assets/Reading.jpg'
import Music from '../assets/Music.jpg'
import Knitting from '../assets/Knitting.jpg'
import Crochet from '../assets/Crochet.jpg'
import CardMaking from '../assets/CardMaking.jpg'
import WatchingTv from '../assets/watching_tv.jpg'
import CrossStitch from '../assets/CrossStitch.jpg'
import Painting from '../assets/Painting.jpg'
import '../css/ActivityCard.css'

const ActivityCard = ({ Name, Type, Image, onClick }) => {

    return (
        <div className='activity-card' onClick={onClick}>
            <div className='activity-card-header'>
                <div className='activity-card-title-group'>
                    <h5 className='activity-card-title'>{Name}</h5>
                </div>
            </div>
            {Name === 'Walking' && <img className='activity-card-image' src={Walking} alt={Name} />}
            {Name === 'Jogging' && <img className='activity-card-image' src={Jogging} alt={Name} />}
            {Name === 'Model Building' && <img className='activity-card-image' src={ModelBuilding} alt={Name} />}
            {Name === 'Origami' && <img className='activity-card-image' src={Origami} alt={Name} />}
            {Name === 'Gardening' && <img className='activity-card-image' src={Gardening} alt={Name} />}
            {Name === 'Yoga' && <img className='activity-card-image' src={Yoga} alt={Name} />}
            {Name === 'Reading' && <img className='activity-card-image' src={Reading} alt={Name} />}
            {Name === 'Listening to Music or Podcasts' && <img className='activity-card-image' src={Music} alt={Name} />}
            {Name === 'Knitting' && <img className='activity-card-image' src={Knitting} alt={Name} />}
            {Name === 'Crochet' && <img className='activity-card-image' src={Crochet} alt={Name} />}
            {Name === 'Card making' && <img className='activity-card-image' src={CardMaking} alt={Name} />}
            {Name === 'Watching Movies or TV Shows' && <img className='activity-card-image' src={WatchingTv} alt={Name} />}
            {Name.includes('Cross Stitch') && <img className='activity-card-image' src={CrossStitch} alt={Name} />}
            {Name.includes('Painting') && <img className='activity-card-image' src={Painting} alt={Name} />}
            {Type.includes('exercise') && <img className='activity-card-image' src={Image} alt={Name} />}
            {Type.includes('Yoga') && <img className='activity-card-image' src={Image} alt={Name} />}
            <div className='activity-card-text fst-italic' style={{ fontSize: 'x-large' }}><span style={{ fontWeight: 'bold' }}>Type: </span>{Type}</div>
        </div>
    )
}

export default ActivityCard