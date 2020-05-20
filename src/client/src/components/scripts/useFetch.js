import React, { useState, useEffect } from 'react';

export default function useFetch (initialUrl, initialData){

    const [data, setData] = useState(initialData);
    const [url, setUrl] = useState(initialUrl);
    const [isLoading, setIsLoading] = useState(false);
    const [isError, setIsError] = useState(false);

    useEffect(() => {
        const fetchData = async ()=>{
            setIsLoading(true);
            setIsError(false);
            
            try{
                fetch(url)
                    .then(res => res.json())
                    .then(d => {setData(d)});
            }
            catch(error){
                setIsError(true);
            }
        setIsLoading(false);
        };
        fetchData();
    }, [url]);

    return [{data, isLoading, isError}, setUrl];
}