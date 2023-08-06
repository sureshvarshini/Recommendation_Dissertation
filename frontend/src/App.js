import 'bootstrap/dist/css/bootstrap.min.css'
import './css/main.css'
import React, { useEffect, useState } from 'react'
import {
  BrowserRouter as Router,
  Routes,
  Route
} from 'react-router-dom';
import { Modal } from 'react-bootstrap'
import { Link } from 'react-router-dom'
import Navbar from './components/Navbar'
import HomePage from './components/Home'
import SignupPage from './components/SignUp'
import LoginPage from './components/Login'
import MyAccountPage from './components/MyAccount'
import GoodbyePage from './components/Goodbye'
import RecipeRecommendationPage from './components/RecipeRecommendation'
import WaterTrackerPage from './components/WaterTracker'
import ActivityRecommendationPage from './components/ActivityRecommendation'
import glassWater from "./assets/glass_water.jpg"

function App() {

  const [showReminder, setShowReminder] = useState(false);

  const closeReminder = () => {
    setShowReminder(false);
  };

  useEffect(() => {
    const interval = setInterval(() => {
      console.log('Calling water reminder pop up.')
      setShowReminder(true);
    }, 2 * 60 * 1000);
    return () => clearInterval(interval);
  }, [])

  return (
    <>
      <Router>
        <div className='app'>
          <Navbar />
          <Routes>
            <Route path='/recommendations/activity' element={<ActivityRecommendationPage />} />
            <Route path='/recommendations/food' element={<RecipeRecommendationPage />} />
            <Route path='/recommendations/water' element={<WaterTrackerPage />} />
            <Route path='/enduser' element={<GoodbyePage />} />
            <Route path='/myaccount' element={<MyAccountPage />} />
            <Route path='/login' element={<LoginPage />} />
            <Route path='/signup' element={<SignupPage />} />
            <Route path='/' element={<HomePage />} />
          </Routes>
        </div>
        {showReminder &&
          <Modal show={showReminder} size="lg" onHide={closeReminder} onClick={closeReminder} style={{ padding: 100 }}>
            <Modal.Header closeButton>
              <Modal.Title style={{ fontWeight: 'bold' }}>
                Hydration time! Grab a glass of water.
              </Modal.Title>
            </Modal.Header>
            <Modal.Body style={{ fontSize: '20px' }}>
              <div className="d-flex justify-content-center">
                <img className='glass-water' src={glassWater} alt='glass-water' style={{ width: "400px", height: "auto" }} />
              </div>
              <div className="d-flex justify-content-center">
                <p style={{ fontSize: "30px" }}>Log water <Link to='/recommendations/water' style={{ fontWeight: 'bold' }}>here</Link></p>
              </div>
            </Modal.Body>
          </Modal>}
      </Router>
    </>
  );
}

export default App
