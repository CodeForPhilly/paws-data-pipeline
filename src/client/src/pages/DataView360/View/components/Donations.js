import React, {Component} from 'react';
import {
    Paper,
    Typography,
    Table,
    TableContainer,
    TableHead,
    TableBody,
    TableRow,
    TableCell,
    Container
} from '@material-ui/core';
import {withStyles} from '@material-ui/core/styles';
import _ from 'lodash';
import moment from 'moment';
import AttachMoneyIcon from '@material-ui/icons/AttachMoney';
import Grid from "@material-ui/core/Grid";


const customStyles = theme => ({
    spaceIcon: {
        marginTop: 3,
        marginRight: 3
    },
    headerCell: {
        fontWeight: "bold",
    }
});

const ROWS_TO_SHOW = 3

class Donations extends Component {
    constructor(props) {
        super(props);

        this.createRows = this.createRows.bind(this);
    }

    createRows(donations) {
        const donationsSorted = _.sortBy(donations, donation => {
            return new moment(donation.close_date).format("YYYY-MM-DD");
        }).reverse();

        const latestDonations = donationsSorted.slice(0, ROWS_TO_SHOW);

        const result = _.map(latestDonations, (donation, index) => {
            return (<TableRow key={index}>
                <TableCell>{donation.close_date}</TableCell>
                <TableCell>${donation.amount}</TableCell>
                <TableCell>{donation.type}</TableCell>
                <TableCell>{donation.primary_campaign_source}</TableCell>
            </TableRow>);
        });

        return result;
    }

    render() {
        const {classes} = this.props;
        const headerText = `Financial Support Activity (Most Recent ${ROWS_TO_SHOW})`
        return (
            <Container component={Paper} style={{"marginTop": "1em"}}>
                <Typography variant='h5'>
                    <Grid container style={{"margin": "0.5em"}} direction={'row'}>
                        <Grid item className={classes.spaceIcon}>
                            <AttachMoneyIcon color='primary' fontSize='inherit'/>
                        </Grid>
                        <Grid item>
                            {headerText}
                        </Grid>
                    </Grid>
                </Typography>

                <TableContainer component={Paper} style={{"marginBottom": "1em"}} variant='outlined'>
                    <Table>
                        <TableHead>
                            <TableRow>
                                <TableCell className={classes.headerCell}>Date of Donation</TableCell>
                                <TableCell className={classes.headerCell}>Amount</TableCell>
                                <TableCell className={classes.headerCell}>Donation Type</TableCell>
                                <TableCell className={classes.headerCell}>Primary Campaign Source</TableCell>
                            </TableRow>
                        </TableHead>
                        <TableBody>
                            {this.props.donations && this.createRows(this.props.donations)}
                        </TableBody>
                    </Table>
                </TableContainer>
            </Container>
        );
    }
}


export default withStyles(customStyles)(Donations);