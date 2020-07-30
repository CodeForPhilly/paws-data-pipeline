import  React from "react";
import { Link as RouterLink } from "react-router-dom";
import {AppBar, Button, Toolbar, Typography } from "@material-ui/core";

export default function Header(props){

  return(
        <AppBar position="static" id="header" color="primary" elevation={1}> 
          <Toolbar style={{"minWidth":"100", "dipslay":"flex", "justifyContent":"space-between"}}>
            <Typography variant="h6">Hello Paws User</Typography>
            <div style={{"display":"flex", "justifyContent":"space-between", "margin":"1em"}}>
              <Button color="default" component={RouterLink} to="/upload">Admin</Button>
              <Button color="default" component={RouterLink} to="/dataView">360 DataView</Button>
              <Button color="default" component={RouterLink} to="/about">About</Button>
            </div>
          </Toolbar>
        </AppBar>
  );
}
