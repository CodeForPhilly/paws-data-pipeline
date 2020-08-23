const proxy = require('http-proxy-middleware');


module.exports = function(app) {
    app.use(proxy('/api/**', {
            //target: 'http://localhost:3333'
            target: 'http://server:5000'
        }
    ));
}