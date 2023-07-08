import React from "react";
import { Link } from "react-router-dom";

const HomePage = () => {
    return(
        <div className="Home container">
            <h1>Welcome to AssistWise</h1>
            <h3>Let's begin your personalized recommendations journey. The first step is just a click away.</h3>
            <Link to='/signup' className="btn btn-primary">Get started now.</Link>
        </div>
    )
}

export default HomePage