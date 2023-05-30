# Accessing APIs without React
test
As of [c863c77](https://github.com/CodeForPhilly/paws-data-pipeline/commit/c863c77cfb79901f65936a851834ec298aec5ec1) , a valid JWT is needed to access API endpoints. If you don't want to use the normal route (React) there are a few options:

* Programmatically through JS: See examples in Login.js, Admin.js, Search.js
* Programmatically through Python: See /server/test\_api.py
* Using Postman

### Using Postman

To use Postman:

* Get a valid JWT, which is returned by /api/user/login
  * You can do this through Postman or by capturing the returned `access_token`value using browser devtools

![Postman\_login](https://user-images.githubusercontent.com/11001850/114760059-f0dbf180-9d2c-11eb-83d9-27ea69ceaa66.png)

* Tell Postman to use that value for API calls
  * Copy the value
  * Edit the collection (three dots when hovering to right of collection name, Edit)

![Postman\_view\_more](https://user-images.githubusercontent.com/11001850/114760490-592ad300-9d2d-11eb-935b-2a67220e903c.png)

* Choose Authorization, Type: Bearer Token
* Paste value into the Token field, save

![Postman\_token](https://user-images.githubusercontent.com/11001850/114760547-69db4900-9d2d-11eb-8e2c-779060b81205.png)

Start issuing API calls

### Error codes

401 - Bad login credentials\
403 - Tried to access an Admin endpoint with user-level credentials\
422 - JWT value was corrupted/failed validation
