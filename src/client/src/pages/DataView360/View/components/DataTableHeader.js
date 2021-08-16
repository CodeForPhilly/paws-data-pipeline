import React from 'react';
import {
    Typography,
} from '@material-ui/core';
import Grid from "@material-ui/core/Grid";
import Box from "@material-ui/core/Box";


function DataTableHeader(props) {
    const { headerText, emojiIcon } = props;
    return (
        <Typography variant='subtitle1'>
            <Box pt={1}>
                <Grid container direction={'row'} alignItems="center" alignContent="center">
                    <Grid item>
                        <Box pt={1.2}>
                            {emojiIcon}
                        </Box>

                    </Grid>
                    <Grid item>
                        {headerText}
                    </Grid>
                    <Grid item>
                        {props.children}
                    </Grid>
                </Grid>
            </Box>

        </Typography>
    );
}

export default DataTableHeader;