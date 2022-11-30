# User management and authorization

### Intro

Because the 360 view gives access to sensitive personal information, we need to ensure that only authorized users can access PDP pages.

### Roles

There are three authorization levels/user roles:

* User: Can use the **Common API** to view 360 data but not make any changes
* Editor: User role plus can use the **Editor API** to manually link existing contacts
* Admin: Editor role plus can use the **Admin API** to upload data and manage users

### Login

Upon login, the user API shall return a JSON Web \[Access] Token (JWT) with a limited lifetime\[1]. The JWT includes the user's role.

### Authorization

The React client shall render only resources that are authorized by the current user's role. The React client shall present the JWT (using the **Authorization: Bearer** header) to the API server when making a request.\
The API server shall verify that user represented by the JWT is authorized to access the requested API endpoint. The server API shall return a 403 status if the user is not authorized to access the endpoint.

### Implementation

User roles are stored in the database `pdp_user_roles` table and per-user data is stored in the `pdp_users` table.

### API

**No authorization required**

| Endpoint              | Description                       |
| --------------------- | --------------------------------- |
| `/api/user/test`      | Liveness test, always returns 200 |
| `/api/user/test_fail` | Always fails with 401             |
| `/api/user/login`     | Login                             |

**Valid JWT required**

| Endpoint              | Description                                 |
| --------------------- | ------------------------------------------- |
| `/api/user/test_auth` | Returns 200 if valid JWT presented          |
| `/api/user/logout`    | Logout (optional, as client can delete JWT) |

**Admin role required**

| Endpoint                         | Description                    |
| -------------------------------- | ------------------------------ |
| `/api/admin/user/create`         | Create user                    |
| `/api/admin/user/get_user_count` | Get count of all users in DB   |
| `/api/admin/user/get_users`      | Get list of users with details |



\[1] _We need to decide on a lifetime that provides an appropriate balance between convenience and security. An expired Access token will require the user to login again. There is a Refresh-type token that allows automatic renewal of Access tokens without requiring the user to log in but the power of this kind of token poses additional security concerns._
