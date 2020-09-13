const proxy = require('http-proxy-middleware');


module.exports = function(app) {
    console.log(process.env.IS_LOCAL)
    app.use(proxy('/api/**', {
            target: process.env.IS_LOCAL === true ? 'http://localhost:3333' : 'http://server:5000'
        }
    ));
}