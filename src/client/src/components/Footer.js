import  React from "react";
import { Link as RouterLink } from "react-router-dom";
import {Paper, Toolbar, Link } from "@material-ui/core";


export default function Footer(props){

  return (
      <Paper elevation={1} style={{"marginTop":"1em"}}>
        <Toolbar style={{
              "minWidth":"100",
              "display":"flex",
              "flexDirection":"row",
              "justifyContent":"center"
            }}>
            <div>
              <Link style={{"margin":"1em"}} component={RouterLink} to="/upload">Upload</Link>
              <Link style={{"margin":"1em"}} component={RouterLink} to="/dataview">360 DataView</Link>
              <Link style={{"margin":"1em"}} component={RouterLink} to="/about">About</Link>
            </div>
        </Toolbar>
      </Paper>
  );

}
