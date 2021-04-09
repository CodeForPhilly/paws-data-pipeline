import React from 'react';
import useToken from '../components/Login/useToken';
var jwt = require('jsonwebtoken');


export default async function Refresh(old_token) {

    
        console.log("Top of Refresh, old_token = " + String(old_token).slice(-8) );

        // get the decoded payload and header
        var decoded = jwt.decode(old_token, { complete: true });
        const expTime = decoded?.payload.exp
        // console.log('User: ' + userName + ' / Role:' + userRole + '->' +  processStatus + ' @ ' + DateTime.local().toFormat('HH:mm:ss.SSS'))

    


    //   console.log('authCheck startfetch @ ' + DateTime.local().toFormat('HH:mm:ss.SSS'))
        const new_at = await fetch('http://localhost:5000/api/user/refresh',
        {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + old_token
            }
        })

        .then((response) => {
        //   console.log('authCheck handle response @ ' + DateTime.local().toFormat('HH:mm:ss.SSS'))
            if (!response.ok) {
                //throw (String(response.status + ':' + response.statusText))
                throw (response)
            }
            return response.json()
        } )

        .catch((e) => {
            // If it failed there's not much to do, probably got here after expiration 
            console.log(String(e)); 
            return '{}'
        });

        console.log(">>>>>>>>>>>>>>>>>>>> Refreshed, New AT: " + String(new_at.access_token).slice(-8) );
            
        return(new_at);




}

