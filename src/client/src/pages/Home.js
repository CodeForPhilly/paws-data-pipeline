import React, { Component } from 'react';
import startImage from '../assets/startImage.jpg';
import Grid from '@material-ui/core/Grid';
import { Container } from "@material-ui/core";


class HomePage extends Component {
    render() {
        return (
            <Grid container justify = "center">
                <Container style={{display: "flex",justifyContent: "center", alignItems: "center"}}>
                    <h2>Welcome PAWS User</h2>
                </Container>
                <Container style={{display: "flex",justifyContent: "center", alignItems: "center"}}>
                    <img src={startImage} alt="animal-friends" width="300" height="300"/>
                </Container>
            </Grid>
        );
    }
}

export default HomePage;