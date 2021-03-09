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

// Testing only
const sleep = time => new Promise(resolve => setTimeout(resolve, time))
const getUser = () => sleep(1000).then(() => ({username: 'PAWS_user', role:'admin'})) //.then(() =>  Error)
//  End testing 

const AuthContext = React.createContext()
function AuthProvider({children}) {
  const [state, setState] = React.useState({
    status: 'pending',
    error: null,
    user: null,
  })
  React.useEffect(() => {
    getUser().then(
      user => setState({status: 'success', error: null, user}),
      error => setState({status: 'error', error, user: null}),
    )
  }, [])

  return (
    <AuthContext.Provider value={state}>
      {state.status === 'pending' ? (
        'Loading...'
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



function UnauthenticatedApp() {
  return (
    <>
      <h3>Unauthorized</h3>
    </>
  )
}

function AuthenticatedApp() {

    const {user} = useAuthState()

    const { access_token, setToken } = useToken();

    if (!access_token) {
      return <Login setToken={setToken} />
    }


  return (
    <>
        <Router>
            {user.role === 'admin' ?  <AdminHeader /> : <Header /> }
            <h3>TEST: {user.username} is a {user.role}</h3>
            <Switch>
                <Route exact path="/">
                    <HomePage/>
                </Route>
                {user.role === 'admin' && 
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
        </Router>
    </>
  )
}

function Home() {
  const {user} = useAuthState()
  return user ? <AuthenticatedApp /> : <UnauthenticatedApp />
}

function App() {

  // const {username, role} = useAuthState()

  return (
    <AuthProvider>
      <div>
         {/* <p>(AuthProvider) Hi , you big</p> */}
        <Home />
      </div>
    </AuthProvider>
  )
}

 export default App
