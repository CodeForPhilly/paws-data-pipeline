import React from "react";
import {BrowserRouter as Router, Switch, Route} from 'react-router-dom';

import Header from "./components/Header";

import HomePage from './pages/Home';
import Admin from './pages/Admin';
import DataView from './pages/DataView360/DataView360';
import About from './pages/About';

/*basic routing of the app*/
export default function App(props) {
    return (
        <Router>
            <Header/>
            <Switch>
                <Route exact path="/">
                    <HomePage/>
                </Route>
                <Route path="/admin">
                    <Admin/>
                </Route>
                <Route path="/about">
                    <About/>
                </Route>
                <Route path="/dataView">
                    <DataView/>
                </Route>
            </Switch>
        </Router>
    );
}

