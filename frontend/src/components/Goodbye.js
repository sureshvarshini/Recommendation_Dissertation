import React from 'react'
import { Link } from 'react-router-dom'
import { Form } from 'react-bootstrap'

const GoodbyePage = () => {
    return (
        <div className='container'>
            <h1>Sorry to see you go!</h1>
            <form>
                <Form.Group>
                    <h6>Take me back to <Link to='/'> home</Link>.</h6>
                </Form.Group>
            </form>
        </div>
    )
}

export default GoodbyePage