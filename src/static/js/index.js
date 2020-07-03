import React from "react";
import ReactDOM from "react-dom";
import App from "./App.js";
import {createMuiTheme, ThemeProvider } from '@material-ui/core/styles';

const theme = createMuiTheme({
  palette: {
    primary: {
      light: '#c3fdff',
      main: '#90caf9',
      dark: '#5d99c6',
    },
  },
});

ReactDOM.render(
    (<ThemeProvider theme={theme}>
        <App />
    </ThemeProvider>),
    document.getElementById("root"));