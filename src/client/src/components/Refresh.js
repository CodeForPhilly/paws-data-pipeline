export default async function Refresh(old_token) {
    
    // Use exisiting token to get a new fresh token

        const new_at = await fetch('http://localhost:5000/api/user/refresh',
        {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + old_token
            }
        })

        .then((response) => {
            if (!response.ok) {
                //throw (String(response.status + ':' + response.statusText))
                throw (response)
            }
            return response.json()
        } )

        .catch((e) => {
            // If it failed there's not much to do, probably got here after expiration 
            return '{}'
        });

           
        return(new_at);

}

