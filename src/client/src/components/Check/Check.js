import React from 'react';
import { useHistory } from "react-router-dom";
import useToken from '../Login/useToken';
var jwt = require('jsonwebtoken');

// USeful for generating 'expired token' errors
const old_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTYxNDcxNjk5NCwianRpIjoiY2Y2Y2U5OTAtZGExNS00ZjZmLTljNGUtNzdjZWJjZmFlZjU0IiwibmJmIjoxNjE0NzE2OTk0LCJ0eXBlIjoiYWNjZXNzIiwic3ViIjoiYmFzZV91c2VyIiwiZXhwIjoxNjE0NzE3Mjk0LCJyb2xlIjoidXNlciJ9.WyFfP40lINcjeNvWEmNhoBr1wYyjniNQuIdMjuwyY0s"



export default function Check() {
    const [processStatus, setProcessStatus] = React.useState('loading');
    const [error, setError] = React.useState('');
    const [data, setData] = React.useState('');

    const { access_token, setToken } = useToken();

    let history = useHistory();

    // get the decoded payload and header
    var decoded = jwt.decode(access_token, { complete: true });
    const userName = decoded?.payload.sub
    const userRole = decoded?.payload.role
    console.log('User: ' + userName + ' / Role:' + userRole)

    React.useEffect(() => {
        setProcessStatus('loading');
        fetch('http://localhost:5000/api/user/test_auth',
            {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer ' + access_token
                }
            })

            .then((response) => {

                if (!response.ok) {
                    //throw (String(response.status + ':' + response.statusText))
                    throw (response)
                }
                return response.json()
            }
            )
            .then((data) => {
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
            })
            ;
    }, []);

    if (processStatus === 'loading') {
        console.log('loading...')
        return <p>loading..</p>;
    }

    if (processStatus === 'error') {
        console.log('error')
        return <p>ERROR: <i>{error}</i></p>;
    }

    var jd = parse_jwt(access_token)

    return (
        <div>
            <h2>Check</h2>
            <ul>
                <li>{data}</li>
                <li>User: {jd.sub}</li>
                <li>Role: {jd.role}</li>
                <li>JWT expires: {-(Date.now()/1000 - jd.exp).toFixed(1)} secs</li>

            </ul>
            {userRole === 'admin' &&
                <h2>Welcome, admin!</h2>
            }
        </div>
    );
};

function parse_jwt(token){
    let jstr = atob(token.split('.')[1]);
    let jdict = JSON.parse(jstr);
    return jdict;
}