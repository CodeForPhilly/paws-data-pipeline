import { useState } from 'react';

export default function useToken() {
    const getToken = () => {
        const tokenString = sessionStorage.getItem('access_token');  // getItem(key)
        const userToken = JSON.parse(tokenString);

        console.log("UT - uT:" + String(userToken?.access_token).slice(-9,-1) );
        // if (access_token) console.log("UT AT" +  String(access_token).slice(-9,-1) ) ;

        console.log("Returning AT:" + String(userToken?.access_token).slice(-9,-1));
        return userToken?.access_token
    };


    const [access_token, setToken] = useState(getToken());

    const saveToken = userToken => {
        sessionStorage.setItem('access_token', JSON.stringify(userToken));
        setToken(userToken?.access_token);
    };


    return {
        setToken: saveToken,
        access_token
    }


}