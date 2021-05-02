import React from 'react';
import {
    Typography,
} from '@material-ui/core';
import { makeStyles, withStyles } from '@material-ui/core/styles';
import Grid from "@material-ui/core/Grid";


const customStyles = makeStyles({
    spaceIcon: {
        marginTop: 3,
        marginRight: 3
    },
    headerCell: {
        fontWeight: "bold"
    },
});

function DataTableHeader(props) {
    const classes = customStyles();
    const { headerText, emojiIcon } = props;
    return (
        <Typography variant='h5'>
            <Grid container style={{ "margin": "0.5em" }} direction={'row'}>
                <Grid item className={classes.spaceIcon}>
                    { emojiIcon }
                </Grid>
                <Grid item>
                    { headerText }
                </Grid>
                { props.children }
            </Grid>
        </Typography>
    );
}

export default withStyles(customStyles)(DataTableHeader);