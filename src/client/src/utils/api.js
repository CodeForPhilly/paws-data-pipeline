export const fetchUsers = async ({ token }) => {
    const api = "/api/admin/user/get_users";
    const requestOptions = {
        method: 'GET',
        headers: {
            'Authorization': 'Bearer ' + token
        },
    };

    return fetch(api, requestOptions)
        .then((res) => res.json())
        .catch((e) => {
            console.warn(e)
            throw new Error(e);
        })
            
}