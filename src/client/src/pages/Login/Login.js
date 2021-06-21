import React, {useState} from 'react';
import PropTypes from 'prop-types';
import {CardContent, Paper, TextField, Typography} from "@material-ui/core";
import Grid from "@material-ui/core/Grid";
import Button from "@material-ui/core/Button";

function checkLoginResponse(response) {
    let gotError = !response.ok;
    if (gotError) {
        throw new Error("Unable to log in - check username and password");
    }
    return response
}


async function loginUser(credentials) {
    return fetch('/api/user/login', {
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

export default function Login({setToken}) {
    const [username, setUserName] = useState();
    const [password, setPassword] = useState();
    //const [authcode, setAuthCode] = useState();  // For future use

    const handleSubmit = async e => {
        e.preventDefault();
        const access_token = await loginUser({
            username,
            password
        });
        setToken(access_token);
    }

    return (
        <Grid container direction="column" alignItems="center" spacing={3}>
            <Grid item>
                <Typography variant={"h2"}>Please Log In</Typography>
            </Grid>
            <Grid item>
                <Paper style={{width: 500}}>
                    <CardContent>
                        <form onSubmit={handleSubmit}>
                            <Grid item container direction="column" spacing={3}>
                                <Grid item>
                                    <TextField fullWidth type="text" label="User Name"
                                               onChange={e => setUserName(e.target.value)}/>
                                </Grid>
                                <Grid item>
                                    <TextField fullWidth type="password" label="Password"
                                               onChange={e => setPassword(e.target.value)}/>
                                </Grid>
                                <Grid item>
                                    <Button color="primary" variant="contained" type="submit">Submit</Button>
                                </Grid>
                            </Grid>

                        </form>
                        <Typography style={{paddingTop: 10, color: 'red'}} id="loginErrorMsg"></Typography>
                    </CardContent>

                </Paper>
            </Grid>
        </Grid>
    )
}

Login.propTypes = {
    setToken: PropTypes.func.isRequired
};