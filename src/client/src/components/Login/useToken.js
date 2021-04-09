import { useState } from 'react';

export default function useToken() {
    const getToken = () => {
        const tokenString = sessionStorage.getItem('access_token');  // getItem(key)
        const userToken = JSON.parse(tokenString);

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