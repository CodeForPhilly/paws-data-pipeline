import React from "react";
import {Link as RouterLink} from "react-router-dom";
import {AppBar, Button, Toolbar, Typography} from "@material-ui/core";
import styles from "./styles/header.module.css";
import admstyles from "./styles/adm_header.module.css";

export function AdminHeader(props) {  // This one if user has the ADMIN role

    return (
        <AppBar position="static" id="header" className={admstyles.header} elevation={1}>
            <Toolbar style={{"minWidth": "100", "dipslay": "flex", "justifyContent": "space-between"}}>
                <Button className={styles.header_link} component={RouterLink} to="/">
                    <Typography className={styles.header_logo} variant="h6">PAWS Data Pipeline</Typography>
                </Button>

                <div style={{"display": "flex", "justifyContent": "space-between", "margin": "16px 6px 16px 16px"}}>

                    <Button className={styles.header_link} component={RouterLink} to="/admin">Admin</Button>
                    <Button className={styles.header_link} component={RouterLink} to="/360view/search">360
                        DataView</Button>
                    <Button className={styles.header_link} component={RouterLink} to="/about">About us</Button>
                    { /* <Button className={styles.header_link} component={RouterLink} to="/check">Check</Button> */}
                </div>
            </Toolbar>
        </AppBar>
    );
}

export function LoginHeader(props) {  // This one for login page

    return (
        <AppBar position="static" id="header" className={styles.header} elevation={1}>
            <Toolbar style={{"minWidth": "100", "dipslay": "flex", "justifyContent": "space-between"}}>
                <Typography className={styles.header_logo} variant="h6">PAWS Data Pipeline</Typography>
                <div style={{"display": "flex", "justifyContent": "space-between", "margin": "16px 6px 16px 16px"}}>
                    <Button className={styles.header_link} component={RouterLink} to="/about">About us</Button>
                    { /* <Button className={styles.header_link} component={RouterLink} to="/check">Check</Button> */}
                </div>
            </Toolbar>
        </AppBar>
    );
}


export default function Header(props) {  // This one if user only has USER role - no link to Admin page

    return (
        <AppBar position="static" id="header" className={styles.header} elevation={1}>
            <Toolbar style={{"minWidth": "100", "dipslay": "flex", "justifyContent": "space-between"}}>
                <Typography className={styles.header_logo} variant="h6">PAWS Data Pipeline</Typography>
                <div style={{"display": "flex", "justifyContent": "space-between", "margin": "16px 6px 16px 16px"}}>
                    <Button className={styles.header_link} component={RouterLink} to="/360view/search">360
                        DataView</Button>
                    <Button className={styles.header_link} component={RouterLink} to="/about">About us</Button>
                    { /* <Button className={styles.header_link} component={RouterLink} to="/check">Check</Button> */}
                </div>
            </Toolbar>
        </AppBar>
    );
}

