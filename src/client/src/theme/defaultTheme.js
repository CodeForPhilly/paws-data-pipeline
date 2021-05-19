import {createMuiTheme} from '@material-ui/core/styles';

//@link https://cimdalli.github.io/mui-theme-generator/
//@todo set overrides for all core components,
// need to make sure imported components implement theming


const defaultTheme = createMuiTheme({
    palette: {
        primary: {
            main: '#90caf9',
            contrastText: '#fff',
        },
        secondary: {
            main: '#f44336',
            contrastText: '#000',
        }
    },
    typography: {
        fontFamily: [
            '-apple-system',
            'BlinkMacSystemFont',
            '"Segoe UI"',
            'Roboto',
            '"Helvetica Neue"',
            'Arial',
            'sans-serif',
            '"Apple Color Emoji"',
            '"Segoe UI Emoji"',
            '"Segoe UI Symbol"',
        ].join(','),
    }
});

defaultTheme.overrides = {
    MuiSvgIcon: {
        root: {
            padding: 5
        }
    }
};

export default defaultTheme;