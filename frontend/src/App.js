import 'bootstrap/dist/css/bootstrap.min.css';
import './css/main.css'
import React, { useEffect, useState } from 'react';
import axios from 'axios'
import { 
  BrowserRouter as Router, 
  Routes, 
  Route
} from 'react-router-dom';
import Navbar from './components/Navbar';
import HomePage from './components/Home';
import SignupPage from './components/SignUp';
import LoginPage from './components/Login';

function App() {
  const [data, setData] = useState({})

  useEffect(() => {
    axios.get('http://localhost:5000/test').then(response => {
      console.log("Success from fetching from test endpoint", response)
      setData(response)
    }).catch(error => {
      console.log(error)
    })

  }, [])

  return (
    <>
    <Router>
      <div className=''>
        <Navbar />
        <Routes>
          <Route path='/login' element={<LoginPage />} />
          <Route path='/signup' element={<SignupPage />} />
          <Route path='/'  element={<HomePage />} />
        </Routes>
        <header className="App-header">
          <p>Recommendation Application</p>
          <div>{data.status === 200 ? <h3>{data.data.message}</h3> : <h3>LOADING</h3>}</div>
        </header>
      </div>
    </Router>
    </>
  );
}

export default App;
