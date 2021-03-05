import React from 'react'

import {BrowserRouter as Router, Switch, Route} from 'react-router-dom';

import Header, {AdminHeader} from "./components/Header";

import HomePage from './pages/Home';
import Admin from './pages/Admin';
import DataView from './pages/DataView360/DataView360';
import About from './pages/About';


const sleep = time => new Promise(resolve => setTimeout(resolve, time))

const getUser = () => sleep(1000).then(() => ({username: 'PAWS_user', role:'admin'})) //.then(() =>  Error)

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

function Footer() {
  return <p>This is an awesome app!</p>
}

// function Header() {
//   const {user} = useAuthState()
//   return <p>Hello {user.username}</p>
// }

function Content() {
  const {user} = useAuthState()
  return <p>I am so happy to have you here as a  {user.role}.</p>
}

function UnauthenticatedHeader() {
  return <p>Please login</p>
}

function UnauthenticatedContent() {
  return <p>You must login to read the message</p>
}

function UnauthenticatedApp() {
  return (
    <>
      <UnauthenticatedHeader />
      <UnauthenticatedContent />
    </>
  )
}

function AuthenticatedApp() {

    const {user} = useAuthState()


  return (
    <>
<Router>
            {user.role == 'admin' ?  <AdminHeader/> : <Header /> }
            <h3>{user.username} is a {user.role}</h3>
            <Switch>
                <Route exact path="/">
                    <HomePage/>
                </Route>
                {user.role == 'admin' && 
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
