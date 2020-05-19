import React, { useState, useEffect } from 'react';

const useFetch = (initialUrl, initialData) => {

    const [data, setData] = useState(initialData);
    const [url, setUrl] = useState(initialUrl);
    const [isLoading, setIsLoading] = useState(false);
    const [isError, setIsError] = useState(false);

    

}