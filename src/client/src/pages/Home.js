import React, { Component } from 'react';
import startImage from '../assets/startImage.jpg';
import Grid from '@material-ui/core/Grid';
import {Typography} from "@material-ui/core";


class HomePage extends Component {
    render() {
        return (
            <Grid container direction="column" alignItems="center" spacing={4}>
                <Grid item>
                    <Typography variant="h1" >Welcome PAWS User</Typography>
                </Grid>
                <Grid item>
                    <img src={startImage} alt="animal-friends" width="300" height="300"/>
                </Grid>
            </Grid>
        );
    }
}

export default HomePage;