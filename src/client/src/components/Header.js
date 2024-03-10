import React, {Component} from "react";
import {Link as RouterLink} from "react-router-dom";
import {AppBar, Button, Toolbar, Typography} from "@material-ui/core";
import logo from '../assets/header-logo.png';
import Grid from "@material-ui/core/Grid";

class Header extends Component {
    render() {
        return (
            <AppBar position="static" elevation={1} color={this.props.headerType === 'Admin' ? 'secondary' : 'primary'}>
                <Toolbar>
                    <Grid container direction="row" justify="space-between" alignItems="center">
                        <Grid item>
                            <Button component={RouterLink} to="/">
                                <Grid container direction="row" spacing={2} justify="space-between" alignItems="center">
                                    <Grid item>
                                        <img src={logo} alt="logo" height={35}/>
                                    </Grid>
                                    <Grid item>
                                        <Typography variant="h5">PAWS Data Pipeline</Typography>
                                    </Grid>
                                </Grid>
                            </Button>
                        </Grid>
                        <Grid item>
                            {this.props.headerType === 'Admin' &&
                            <Button size="large" component={RouterLink} to="/admin">Admin</Button>}

                            {this.props.headerType === 'Admin' &&
                            <Button size="large" component={RouterLink} to="/users">Users</Button>}

                            {this.props.headerType !== 'Login' && <Button size="large" component={RouterLink} to="/360view/search">360
                                DataView</Button>
                            }
                            <Button size="large" component={RouterLink} to="/about">About us</Button>
                            {this.props.headerType !== 'Login' &&
                            <Button size="large" component={RouterLink} to="/logout">Log Out</Button>}
                        </Grid>
                    </Grid>
                </Toolbar>
            </AppBar>
        );
    }

}

export default Header;

