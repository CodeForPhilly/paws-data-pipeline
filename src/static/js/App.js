import  React, { useState } from "react";
import { BrowserRouter as Router, Switch, Route } from 'react-router-dom';
import {AppBar, Box, Input, IconButton, Grid, Menu, MenuItem, Toolbar, Paper, Select, FormControl, InputLabel, Tabs, Tab, Container } from "@material-ui/core";
import Skeleton from "@material-ui/lab/Skeleton";
import { makeStyles } from "@material-ui/core/styles";

import Header from "./components/Header";
import Footer from "./components/Footer";

/* 
  It seems to make the most sense to use the Material UI style features when possible. Rather than
fighting with the CSS specificity, or using the id to style every component.
"CSS injected into the DOM by Material-UI to style a component has the highest specificity possible"
https://material-ui.com/customization/components/ 
*/

const useStyles = makeStyles({
    content:{
      minHeight: '95vh'
    },
    paper:{
      minHeight: '95vh',
      backgroundImage: '../../../public/background.jpg'
    }

});



function Content(props){
    const [activeIndex, setActiveIndex] = React.useState(0);
    const classes = useStyles();

    const handleChange = (event, newIndex) => {
        setActiveIndex(newIndex)
    };

    return (
      <Container classes={classes.content}>
        <Tabs value={activeIndex} onChange={handleChange} aria-label="upload-download-reports-tabs">
          <Tab label="Upload" />
          <Tab label="Download" />
          <Tab label="Reports" />
        </Tabs>
        <TabPanel value={activeIndex} index={0}> 
          <Skeleton variant="rect" width={400} height={400}> Select File to Load</Skeleton>
          <UploadForm />
        </TabPanel>
        <TabPanel value={activeIndex} index={1}>
          <Skeleton variant="rect" width={400} height={400}>Select File to Load</Skeleton>
          <DownloadForm />
        </TabPanel>
        <TabPanel value={activeIndex} index={2}>
          <Skeleton variant="rect" width={400} height={400}>Select File to Load</Skeleton>
        </TabPanel>
      </Container>
    );
}

/* Handles the visibility of each tab. By checking index against selected value in parent component */
function TabPanel (props) {
    const { children, value, index } = props;

    return (
        <div className="tab-panel" role="tabpanel" hidden={value !== index} id={'upload-download-reports-tab-${index}'}>
          {children}
        </div>

    )

}

/* These "forms" can be refactored to be a resuable component */
function DownloadForm(props) {

  return (
    <FormControl>
      <InputLabel id="download-source-select-label">Select Download Source</InputLabel>
      <Select labelId="download-source-select-label">
        <MenuItem>Current Items</MenuItem>
        <MenuItem>Archived</MenuItem>
        <MenuItem>Other</MenuItem>
      </Select>
      <Input inputComponent="input" type="file" />
    </FormControl>
  );

}

function UploadForm(props) {

  return (
    <FormControl>
      <InputLabel id="upload-source-select-label">Select Input Source</InputLabel>
      <Select labelId="upload-source-select-label">
        <MenuItem>Salesforce</MenuItem>
        <MenuItem>Volgistics</MenuItem>
        <MenuItem>Petpoint</MenuItem>
      </Select>
      <Input inputComponent="input" type="file" />
    </FormControl>
  );

}

/* Debating between a full sidebar or just a basic dropdown menu */
function Sidebar(props){
  const classes = useStyles();
  return <Paper elevation={3} className={classes.sidebar} >Sidebar</Paper>
}


function Startpage(props) {
  const classes = useStyles();
  return <Paper elevation={3} classes={classes.paper} />
}

/*basic routing of the app */
export default function App(props){
  return (
    <Router>
      <Grid direction="row" spacing={2}>
          <Grid direction="row">
            <Header />
            <Switch>
              <Route exact path="/">
                <Startpage />
              </Route>
              <Route path="/upload">
                <Content />
              </Route>
              <Route path="/about">
                <h1>About Section</h1>
              </Route>
            </Switch>
            <Footer id="footer" />
          </Grid>
        </Grid>
    </Router>
  );
}

