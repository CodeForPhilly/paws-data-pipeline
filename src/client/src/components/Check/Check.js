import React from 'react';
import { useHistory } from "react-router-dom";
import useToken from '../Login/useToken';
var jwt = require('jsonwebtoken');

const { DateTime } = require("luxon");

// USeful for generating 'expired token' errors
const old_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTYxNDcxNjk5NCwianRpIjoiY2Y2Y2U5OTAtZGExNS00ZjZmLTljNGUtNzdjZWJjZmFlZjU0IiwibmJmIjoxNjE0NzE2OTk0LCJ0eXBlIjoiYWNjZXNzIiwic3ViIjoiYmFzZV91c2VyIiwiZXhwIjoxNjE0NzE3Mjk0LCJyb2xlIjoidXNlciJ9.WyFfP40lINcjeNvWEmNhoBr1wYyjniNQuIdMjuwyY0s"










export default function Check() {

    const { access_token, setToken } = useToken();

    const [processStatus, setProcessStatus] = React.useState('loading');
    const [error, setError] = React.useState('');
    const [data, setData] = React.useState('');

    let history = useHistory()
 
    function authCheck() {
        console.log('authCheck startfetch @ ' + DateTime.local().toFormat('HH:mm:ss.SSS'))
        fetch('http://localhost:5000/api/user/test_auth',
        {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + access_token
            }
        })
    
        .then((response) => {
            console.log('authCheck handle response @ ' + DateTime.local().toFormat('HH:mm:ss.SSS'))
            if (!response.ok) {
                //throw (String(response.status + ':' + response.statusText))
                throw (response)
            }
            return response.json()
        } )
        .then((data) => {
            console.log('authCheck data  @ ' + DateTime.local().toFormat('HH:mm:ss.SSS'))
            setProcessStatus('complete');
            setData(data);
        })
        .catch((e) => {
            let errCode = e.status
            let errText = e.statusText
    
            setToken(null)  // Clear the token to force login again
            let errStr = String(e)
            setProcessStatus('error');
            setError(errStr);
            console.log(errCode + ':' + errText)
            history.push('/')
            return e
        });
    
    }  // 

   

    // get the decoded payload and header
    var decoded = jwt.decode(access_token, { complete: true });
    const userName = decoded?.payload.sub
    const userRole = decoded?.payload.role
    const expTime = decoded?.payload.exp
    console.log('User: ' + userName + ' / Role:' + userRole + '->' +  processStatus + ' @ ' + DateTime.local().toFormat('HH:mm:ss.SSS'))


   

    React.useEffect(() => {


        if (! access_token){
           console.log("In Check w/o a token")
        }

    console.log('Running authCheck @ ' + DateTime.local().toFormat('HH:mm:ss.SSS'))
     authCheck();
    console.log('After authCheck @ ' + DateTime.local().toFormat('HH:mm:ss.SSS'))

           
    }, [ processStatus, access_token]);

    // if (processStatus === 'loading') {
    //     console.log('Check: if pc=l loading...')
    //     return <p>loading..</p>;
    // }

    if (processStatus === 'error') {
        console.log('error')
        return <p>ERROR: <i>{error}</i></p>;
    }



    console.log("About to return")
    return (
        <div>
            <h2>Check</h2>
            <ul>
               
            <li>User: {userName}</li>
            <li>Role: {userRole}</li>
            <li>JWT expires: {-(Date.now()/1000 - expTime).toFixed(1)} secs</li>
            <li>{data}</li>

            </ul>
            {userRole === 'admin' &&
                <h2>Welcome, admin!</h2>
            }
        </div>
    );



};

