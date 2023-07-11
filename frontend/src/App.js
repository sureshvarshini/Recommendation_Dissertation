import 'bootstrap/dist/css/bootstrap.min.css'
import './css/main.css'
import React from 'react'
import {
  BrowserRouter as Router,
  Routes,
  Route
} from 'react-router-dom';
import Navbar from './components/Navbar'
import HomePage from './components/Home'
import SignupPage from './components/SignUp'
import LoginPage from './components/Login'
import MyAccountPage from './components/MyAccount'
import GoodbyePage from './components/Goodbye'

function App() {

  return (
    <>
      <Router>
        <div className=''>
          <Navbar />
          <Routes>
            <Route path='/enduser' element={<GoodbyePage />} />
            <Route path='/myaccount' element={<MyAccountPage />} />
            <Route path='/login' element={<LoginPage />} />
            <Route path='/signup' element={<SignupPage />} />
            <Route path='/' element={<HomePage />} />
          </Routes>
        </div>
      </Router>
    </>
  );
}

export default App
