import React from 'react';
import ReactDOM from 'react-dom';
import App from './App';
import { ThemeProvider } from '@material-ui/core/styles';
import * as serviceWorker from './serviceWorker';
import "./assets/font/font.css";
import defaultTheme from './theme/defaultTheme';
import { AlertProvider } from './contexts/AlertContext';
import "process/browser";

ReactDOM.render(
  <React.StrictMode>
    <ThemeProvider theme={defaultTheme}>
      <AlertProvider>
        <App/>
      </AlertProvider>
    </ThemeProvider>
  </React.StrictMode>,
  document.getElementById('root')
);

// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
serviceWorker.unregister();
