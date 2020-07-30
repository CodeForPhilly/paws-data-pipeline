import  React from "react";
import { BrowserRouter as Router, Switch, Route } from 'react-router-dom';

import Header from "./components/Header";

import Startpage from './pages/Start';
import Content from './pages/Upload';
import Dataview from './pages/DataView360';
import About from './pages/About';

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
            <Switch>
              <Route exact path="/">
                <Header />
                <Startpage />
              </Route>
              <Route path="/upload">
                <Header />
                <Content />
              </Route>
              <Route path="/about">
                <Header />
                <About />
              </Route>
              <Route path="/dataview">
                <Header />
                <Dataview />
              </Route>
            </Switch>
    </Router>
  );
}

