import  React, { useState } from "react";
import {AppBar, IconButton, Menu, MenuItem, Toolbar } from "@material-ui/core";
import MenuIcon from "@material-ui/icons/Menu";

export default function Header(props){

  const [anchorEl, setAnchorEl] = useState(null);

  const handleMenuClick = (e) => {
   setAnchorEl(e.target);
  }

  const handleClose = () => {
    setAnchorEl(null);
  }
 

  return(
        <AppBar position="sticky" id="header" color="primary"> 
          <Toolbar>
            <IconButton edge="start" color="inherit" onClick={handleMenuClick}>
              <MenuIcon />
            </IconButton>
            <h1>Hello Paws User</h1>
            <Menu anchorEl={anchorEl}
                  anchorOrigin={{
                    vertical: 'bottom',
                    horizontal: 'center'
                  }} 
                  open={Boolean(anchorEl)}
                  onClose={handleClose}>

                <MenuItem onClick={handleClose}><a href="/upload">Upload</a></MenuItem>
                <MenuItem><a href="/">R5</a></MenuItem>
                <MenuItem><a href="/dataview">360 View</a></MenuItem>
                <MenuItem>R7</MenuItem>
                <MenuItem><a href="/about">About</a></MenuItem>
            </Menu>
          </Toolbar>
        </AppBar>
  );
}
