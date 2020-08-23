import  React from "react";
import { BrowserRouter as Router, Switch, Route } from 'react-router-dom';

import Header from "./components/Header";

import HomePage from './pages/Home';
import Admin from './pages/Admin';
import DataView from './pages/DataView360/DataView360';
import About from './pages/About';

/*basic routing of the app*/ 
export default function App(props){
  return (
    <Router>
            <Switch>
              <Route exact path="/">
                <Header />
                <HomePage />
              </Route>
              <Route path="/upload">
                <Header />
                <Admin />
              </Route>
              <Route path="/about">
                <Header />
                <About />
              </Route>
              <Route path="/dataView">
                <Header />
                <DataView />
              </Route>
            </Switch>
    </Router>
  );
}

