This project was bootstrapped with [Create React App](https://github.com/facebook/create-react-app).

## Proxy Setting 
Proxy setting uses http-proxy-middleware and can be found at `/setupProxy.js`

## Run with docker-compose
The app will be loaded when the docker-compose is ran.   
Open [http://localhost:3000](http://localhost:3000) to view it in the browser.  
In order to view changes, rerun the docker or the whole docker-compose

## Run locally
Make sure proxy is set to the port you are running your backend.  
In the project directory, you can run:   

### `npm start`
This will run locally against the docker container backend which running on port 5000

### `npm run start:local`
This will run locally against your local backend which you should run on port 3333.

## Learn More
You can learn more in the [Create React App documentation](https://facebook.github.io/create-react-app/docs/getting-started).  
To learn React, check out the [React documentation](https://reactjs.org/).  
