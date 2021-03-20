import React from 'react'

import {BrowserRouter as Router, Switch, Route} from 'react-router-dom';

import Header, {AdminHeader} from "./components/Header";

import HomePage from './pages/Home';
import Admin from './pages/Admin';
import DataView from './pages/DataView360/DataView360';
import About from './pages/About';
import Login from './components/Login/Login';
import Check from './components/Check/Check';
import useToken from './components/Login/useToken';
var jwt = require('jsonwebtoken');

// Triggers token expiration check 
const sleep = time => new Promise(resolve => setTimeout(resolve, time))
const expTimer = () => sleep(500).then(() => ({})) 

const AuthContext = React.createContext()

function AuthProvider({children}) {
  const [state, setState] = React.useState({
    status: 'pending',
    error: null,
    user: null,  })

  React.useEffect(() => {
    expTimer().then(
      user => setState({status: 'success', error: null, user})  // 
    )
  }, )

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

    const { access_token, setToken } = useToken();


    var decoded = jwt.decode(access_token, { complete: true });
    const userName = decoded?.payload.sub;
    const userRole = decoded?.payload.role;
    var expTime =  decoded?.payload.exp -  Date.now()/1000;

    const jwtExpired = expTime <= 0

    const hdr = userRole === 'admin' ?  <AdminHeader /> : <Header /> // If we're going to display a header, which one?

  return (
    <>
        <Router>
          
            { !jwtExpired && hdr ?  hdr : '' /* Above-chosen header, or if logged out, no header */ } 
           
            {  /* If not logged in, show login screen */
              (!access_token | jwtExpired) ?  <Login setToken={setToken} /> :    <Switch>  

                <Route exact path="/">
                    <HomePage/>
                </Route>

                {  /* If an admin, render Upload page       */
                  userRole === 'admin' && 
                    <Route path="/upload">
                        <Admin/>
                    </Route>
                    }               

                <Route path="/about">
                    <About/>
                </Route>

                <Route path="/dataView">
                    <DataView/>
                </Route>

                <Route path="/check"> 
                  <Check />
                </Route>
            </Switch>
            }

        </Router>
    </>
  )
}


function Home() {
  const {user} = useAuthState()
  const { access_token, setToken } = useToken();
  return user ? <AuthenticatedApp /> : <Login setToken={setToken} />
}

function App() {
  const { access_token, setToken } = useToken();

  return (
    <AuthProvider>
      <div>
         <Home />
      </div>
    </AuthProvider>
  )
}

 export default App
