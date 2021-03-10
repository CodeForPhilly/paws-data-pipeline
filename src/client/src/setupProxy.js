const proxy = require('http-proxy-middleware');

module.exports = function(app) {
    app.use(proxy('/api/**', {
            target: process.env.IS_LOCAL === 'true' ? 'http://localhost:5000' : 'http://server:5000',
            changeOrigin: true,
        }
    ));
}