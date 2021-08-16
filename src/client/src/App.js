import React from 'react';

import {BrowserRouter as Router, Switch, Route, Redirect} from 'react-router-dom';

import Header from "./components/Header";

import Login from './pages/Login/Login';
import Logout from './pages/Login/Logout';
import HomePage from './pages/Home';
import Admin from './pages/Admin';
import Search360 from './pages/DataView360/Search/Search';
import View360 from './pages/DataView360/View/View360';
import About from './pages/About';
import RefreshDlg from './components/RefreshDlg';
import Check from './pages/Check/Check';
import Refresh from './components/Refresh';

import useToken from './pages/Login/useToken';
import Box from "@material-ui/core/Box";

let jwt = require('jsonwebtoken');

const REFRESH_POPUP_TIME = 300 // seconds

// Triggers token expiration check
const sleep = time => new Promise(resolve => setTimeout(resolve, time))
const expTimer = () => sleep(500).then(() => ({}))

const AuthContext = React.createContext()

function AuthProvider({children}) {
    const [state, setState] = React.useState({
        status: 'pending',
        error: null,
        user: null,
    })

    React.useEffect(() => {
        expTimer().then(
            user => setState({status: 'success', error: null, user})
        )
    },)

    return (
        <AuthContext.Provider value={state}>
            {state.status === 'pending' ? (
                'App ACP: Loading...'
            ) : state.status === 'error' ? (
                <div>
                    Oh no
                    <div>
                        <pre>{state.error.message}</pre>
                    </div>
                </div>
            ) : (
                children
            )}
        </AuthContext.Provider>
    )
}

function useAuthState() {
    const state = React.useContext(AuthContext)
    const isPending = state.status === 'pending'
    const isError = state.status === 'error'
    const isSuccess = state.status === 'success'
    const isAuthenticated = state.user && isSuccess
    return {
        ...state,
        isPending,
        isError,
        isSuccess,
        isAuthenticated,
    }
}


function AuthenticatedApp() {

    const {access_token, setToken} = useToken();

    let decoded = jwt.decode(access_token, {complete: true});

    const userRole = decoded?.payload.role;
    let expTime = decoded?.payload.exp - Date.now() / 1000;
    const jwtExpired = !expTime || expTime <= 0

    const popRefreshAlert = expTime > 0 && expTime < REFRESH_POPUP_TIME;  // Time in secs to pop up refresh dialog

    const headerType = userRole === 'admin' ? 'Admin' : 'Normal';

    return (
        <Router>

            <Box pb={4}>
                {!jwtExpired ? <Header headerType={headerType}/> : <Header headerType={'Login'}/>}
            </Box>
            {popRefreshAlert &&
            <RefreshDlg shouldOpen={true} setToken={setToken}/>} {/* Pop up the refresh dialog */}

            {jwtExpired &&
            <RefreshDlg shouldOpen={false} setToken={setToken}/>} { /* Too late, expired: close the dialog */}


            {  /* If not logged in, show login screen */
                (!access_token | jwtExpired) ?
                    <Switch>
                        <Route path="/about">
                            <About/>
                        </Route>
                        <Route>
                            <Login setToken={setToken}/>
                        </Route>
                    </Switch>

                    : <Switch>
                        <Route exact path="/login">
                            <Redirect to="/"/>
                        </Route>
                        <Route exact path="/">
                            <HomePage access_token={access_token}/>
                        </Route>
                        <Route path="/about">
                            <About/>
                        </Route>

                        {  /* If an admin, render Upload page       */
                            userRole === 'admin' &&
                            <Route path="/admin">
                                <Admin access_token={access_token}/>
                            </Route>
                        }


                        <Route path="/360view/search">
                            <Search360 access_token={access_token}/>
                        </Route>

                        <Route path="/360view/view">
                            <View360 access_token={access_token}/>
                        </Route>

                        <Route path="/check">
                            <Check access_token={access_token}/>
                        </Route>

                        <Route path="/logout">
                            <Logout setToken={setToken}/>
                        </Route>

                        <Route path="/ref">
                            <Refresh/>
                        </Route>

                    </Switch>
            }

        </Router>
    )
}


function Home() {
    const {user} = useAuthState()
    /*eslint no-unused-vars: ["warn", { "varsIgnorePattern": "access_token" }]*/
    const {access_token, setToken} = useToken();
    return user ? <AuthenticatedApp/> : <Login setToken={setToken}/>
}

function App() {

    return (
        <AuthProvider>
            <Home/>
        </AuthProvider>
    )
}

export default App;
