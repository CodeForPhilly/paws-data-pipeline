import  React from "react";
import { Link as RouterLink } from "react-router-dom";
import {Link } from "@material-ui/core";


export default function Footer(props){

  return (
    <div style={{
              "marginTop":"1em",
              "width":"98%",
              "position":"absolute",
              "bottom":"0",
              "display":"flex",
              "flexDirection":"row",
              "justifyContent":"center"
            }}>
        <Link style={{"margin":"1em"}} component={RouterLink} to="/upload">Upload</Link>
        <Link style={{"margin":"1em"}} component={RouterLink} to="/dataview">360 DataView</Link>
        <Link style={{"margin":"1em"}} component={RouterLink} to="/about">About</Link>
    </div>
  );

}
