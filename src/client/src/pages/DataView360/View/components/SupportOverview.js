import React, { Component } from 'react';
import { Box, Container, Divider, Paper, Typography } from '@material-ui/core';
import { withStyles } from '@material-ui/core/styles';

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

    createRowData(data) {
        const isDonor = data.first_donation_date || data.number_of_gifts > 0
        if (!isDonor) {
            return [{"title": "First Gift Date", "value": "N/A"}]
        }
        const rows = [
            { "title": "First Gift Date", "value": data.first_donation_date },
            { "title": "First Gift Amount", "value": `$${data.first_gift_amount}`},
            { "title": "Lifetime Giving", "value": `$${data.total_giving}`},
            { "title": "Total # of Gifts", "value": data.number_of_gifts},
            { "title": "Largest Gift", "value": `$${data.largest_gift}`},
            { "title": "Recurring Donor?", "value": data.is_recurring ? "Yes" : "No"},
            { "title": "RFM Score", "value": data.rfm_score },
            { "title": "RFM Category", "value": data.rfm_label, 
              "rfm_color": data.rfm_color, "rfm_text_color": data.rfm_text_color }
            // { "title": "PAWS Legacy Society?", "value": "test" }
        ]
        return rows;
    }

    createRows(classes, data) {
        return data.map((row) => (
            <Grid container className={classes.spacingRows} direction={'row'} spacing={2} justify={'space-between'} key={row.title} >
                <Grid item>
                    <Typography variant={'body2'} style={{ "fontWeight": "bold" }}>
                        {row.title}
                    </Typography>
                </Grid>
                <Grid item>
                    {(row.rfm_color) 
                    ? <Typography variant={'body2'} align={"right"} style={{ "background": row.rfm_color, "fontColor": row.rfm_text_color }}>
                        {row.value}
                    </Typography>
                    : <Typography variant={'body2'} align={"right"}>
                        {row.value}
                    </Typography>}
                </Grid>
            </Grid>
        ));
    }

    render() {
        const { classes, data } = this.props;
        const rows = this.createRowData(data);

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