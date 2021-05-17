import React from 'react';
import {
    Typography,
} from '@material-ui/core';
import Grid from "@material-ui/core/Grid";


function DataTableHeader(props) {
    const { headerText, emojiIcon } = props;
    return (
        <Typography variant='h5'>
            <Grid container style={{ "margin": "0.5em" }} direction={'row'}>
                <Grid item style={{ "marginTop": "3", "marginRight": "3" }}>
                    {emojiIcon}
                </Grid>
                <Grid item>
                    {headerText}
                </Grid>
                {props.children}
            </Grid>
        </Typography>
    );
}

export default DataTableHeader;