import  React from "react";
import { BrowserRouter as Router, Switch, Route } from 'react-router-dom';
import { Grid } from "@material-ui/core";

import Header from "./components/Header";
import Footer from "./components/Footer";

import Startpage from './pages/Start';
import Content from './pages/Upload';

/* 
  It seems to make the most sense to use the Material UI style features when possible. Rather than
fighting with the CSS specificity, or using the id to style every component.
"CSS injected into the DOM by Material-UI to style a component has the highest specificity possible"
https://material-ui.com/customization/components/ 
*/


/*basic routing of the app*/ 
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

