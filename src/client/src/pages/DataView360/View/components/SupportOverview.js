import React, { Component } from 'react';
import { Box, Container, Divider, Paper, Typography } from '@material-ui/core';
import { withStyles } from '@material-ui/core/styles';

import _ from 'lodash';
import Grid from "@material-ui/core/Grid";

const customStyles = theme => ({
    spacingRows: {
        padding: 2
    },
    spaceIcon: {
        marginTop: 2
    }
});

class SupportOverview extends Component {

    createRowData() {
        const rows = [
            { "title": "First Gift Date", "value": "test" },
            { "title": "First Gift Amount", "value": "test" },
            { "title": "Lifetime Giving", "value": "test" },
            { "title": "Total # of Gifts", "value": "test" },
            { "title": "Largest Gift", "value": "test" },
            { "title": "Recurring Donor?", "value": "test" },
            { "title": "PAWS Legacy Society?", "value": "test" }
        ]
        return rows;
    }

    createRows(classes, data) {
        return data.map((row) => (
            <Grid container className={classes.spacingRows} direction={'row'} spacing={3} justify={'space-between'} key={row.title} >
                <Grid item>
                    <Typography variant={'body2'} style={{ "font-weight": "bold" }}>
                        {row.title}
                    </Typography>
                </Grid>
                <Grid item>
                    <Typography variant={'body2'} align={"right"}>
                        {row.value}
                    </Typography>
                </Grid>
            </Grid>
        ));
    }

    render() {
        const { classes } = this.props;
        const rows = this.createRowData();

        return (
            <Paper elevation={2} style={{ padding: '1em' }}>
                <Container className={classes.containerInfo}>
                    <Grid container direction={'column'}>
                        <Grid container className={classes.spacingRows} direction={'row'} justify='center'>
                            <Grid item>
                                <Typography variant={'subtitle1'}>
                                    <b>Support Overview</b>
                                </Typography>
                            </Grid>
                        </Grid>
                        <Box pb={2}>
                            <Divider />
                        </Box>
                        {this.createRows(classes, rows)}
                    </Grid>
                </Container>

            </Paper>
        );
    }
}

export default withStyles(customStyles)(SupportOverview);