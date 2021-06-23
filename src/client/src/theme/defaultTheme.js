import {createMuiTheme} from '@material-ui/core/styles';


const defaultTheme = createMuiTheme({
    palette: {
        primary: {
            main: '#90caf9',
            contrastText: '#fff',
        },
        secondary: {
            main: '#d9adfa',
            contrastText: '#000',
        },

    },
    typography: {
        fontFamily: 'Roboto',
        htmlFontSize: 16,
        h1: {
            fontSize: '3em',
            fontWeight: 700
        },
        h2: {
            fontSize: '2.5em',
            fontWeight: 700
        },
        h3: {
            fontSize: '2em',
            fontWeight: 700
        },
        h4: {
            fontSize: '1.7em',
            fontWeight: 700
        },
        h5: {
            fontSize: '1.5em',
            fontWeight: 700
        },
        h6: {
            fontSize: '1em',
            fontWeight: 700
        },
        subtitle1: {
            fontSize: '1.5em',
        },
        button: {
            fontSize: '0.8em',
            fontWeight: 700
        },
    }
});

defaultTheme.overrides = {
    MuiSvgIcon: {
        root: {
            padding: 5
        }
    },
    MuiBackdrop: {
        root: {
            zIndex: defaultTheme.zIndex.drawer + 1,
            color: '#fff',
        }

    },
    MuiTableCell: {
        head: {
            fontWeight: "bold"
        }
    },
};

export default defaultTheme;