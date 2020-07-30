import  React from "react";
import { BrowserRouter as Router, Switch, Route } from 'react-router-dom';

import Header from "./components/Header";

import StartPage from './pages/Start';
import Content from './pages/Upload';
import DataView from './pages/DataView360';
import About from './pages/About';

/*basic routing of the app*/ 
export default function App(props){
  return (
    <Router>
            <Switch>
              <Route exact path="/">
                <Header />
                <StartPage />
              </Route>
              <Route path="/upload">
                <Header />
                <Content />
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

