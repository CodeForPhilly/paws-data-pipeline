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

export const createUser = async (userData, token) => {
    const api = "/api/admin/user/create";
    const requestOptions = {
        method: 'POST',
        headers: {
            'Authorization': 'Bearer ' + token
        },
        body: JSON.stringify(userData)
    };

    return fetch(api, requestOptions)
        .then((res) => res.json())
        .catch((e) => {
            console.warn(e)
            throw new Error(e);
        })
}

export const updateUser = async (userData, token) => {
    const api = "/api/admin/user/update";
    const requestOptions = {
        method: 'POST',
        headers: {
            'Authorization': 'Bearer ' + token
        },
        body: JSON.stringify(userData)
    }

    return fetch(api, requestOptions)
        .then((res) => res.json())
        .catch((e) => {
            console.warn(e)
            throw new Error(e);
        })
}
