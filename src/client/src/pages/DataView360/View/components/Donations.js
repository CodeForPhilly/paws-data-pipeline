import React, {Component} from 'react';
import {
    Paper,
    Table,
    TableContainer,
    TableHead,
    TableBody,
    TableRow,
    TableCell,
    Container
} from '@material-ui/core';
import _ from 'lodash';
import moment from 'moment-timezone';
import AttachMoneyIcon from '@material-ui/icons/AttachMoney';
import DataTableHeader from "./DataTableHeader";

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
                <TableCell>${donation.amount.toFixed(2)}</TableCell>
                <TableCell>{donation.type}</TableCell>
                <TableCell>{donation.primary_campaign_source}</TableCell>
            </TableRow>);
        });

        return result;
    }

    render() {
        const headerText = `Financial Support Activity (Most Recent ${ROWS_TO_SHOW})`
        return (
            <Container component={Paper} style={{"marginTop": "1em"}}>
                <DataTableHeader
                    headerText={headerText}
                    emojiIcon={<AttachMoneyIcon color='primary' fontSize='inherit' />}
                />

                <TableContainer component={Paper} variant='outlined' style={{"marginBottom": "1em"}}>
                    <Table>
                        <TableHead>
                            <TableRow>
                                <TableCell>Date of Donation</TableCell>
                                <TableCell>Amount</TableCell>
                                <TableCell>Donation Type</TableCell>
                                <TableCell>Primary Campaign Source</TableCell>
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


export default Donations;