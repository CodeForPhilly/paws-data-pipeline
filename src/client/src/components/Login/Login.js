import React, { useState } from 'react';
import PropTypes from 'prop-types';
import './Login.css';


function checkLoginResponse(response) {
    let gotError = !response.ok;
    if (gotError) {
        throw new Error("Unable to log in - check username and password");
    }
    return response
}


async function loginUser(credentials) {
    return fetch('http://localhost:5000/api/user/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(credentials)
    })
        .then(checkLoginResponse)
        .then(data => data.json())
        .catch(error => document.getElementById('loginErrorMsg').innerHTML = error)

}

export default function Login({ setToken }) {
    const [username, setUserName] = useState();
    const [password, setPassword] = useState();
    // eslint-disable-next-line no-unused-vars
    const [authcode, setAuthCode] = useState();  // For future use

    const handleSubmit = async e => {
        e.preventDefault();
        const access_token = await loginUser({
            username,
            password
        });
        setToken(access_token);
    }

    return (
        <div className="login-wrapper">
            <h1>Please Log In</h1>
            <form onSubmit={handleSubmit}>
                <label>
                    <p>Username</p>
                    <input type="text" onChange={e => setUserName(e.target.value)} />
                </label>
                <label>
                    <p>Password</p>
                    <input type="password" onChange={e => setPassword(e.target.value)} />
                </label>
                {/* <label>
                    <p>Authenticator code</p>
                    <input type="text" placeholder="IGNORE ME"   onChange={e => setAuthCode(e.target.value)} />
                </label> */}
                <div>
                    <button type="submit">Submit</button>
                </div> 
                <div>
                    <p id="loginErrorMsg"></p>
                </div>
            </form>
        </div>
    )
}

Login.propTypes = {
    setToken: PropTypes.func.isRequired
};