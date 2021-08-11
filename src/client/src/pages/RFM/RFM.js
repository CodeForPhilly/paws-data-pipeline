import React from 'react';
import {Container, Divider} from '@material-ui/core';
import _ from 'lodash';
import Typography from "@material-ui/core/Typography";
import Grid from "@material-ui/core/Grid";
import Box from "@material-ui/core/Box";


export function RFM() {
    return (
        <Container>
            <Box display="flex" justifyContent="center" pb={3}>
                <Typography variant={"h2"}>RFM Scores</Typography>
            </Box>
        </Container>

    );
}