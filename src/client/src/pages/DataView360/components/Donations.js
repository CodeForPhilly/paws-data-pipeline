import React, { Component } from 'react';
import { Paper, Typography, Table, TableContainer, TableHead, TableBody, TableRow, TableCell, Container} from '@material-ui/core';
import { withStyles } from '@material-ui/core/styles';
import styles from "./styles/Donations.module.css";
import "./styles/table.css";
import _ from 'lodash';

/* I don't khow, how to remove it. So I changed background-color on 'initial' */
const StyledTableCell = withStyles((theme)=>({
    head:{
        backgroundColor: 'initial', // here
        fontWeight: 600,
    }
}))(TableCell);

const StyledTableRow = withStyles((theme)=>({
    root:{
        '&:nth-of-type(even)':{
            backgroundColor: 'initial', // and here
        }
    }
}))(TableRow);

const ROWS_TO_SHOW = 3

class Donations extends Component {
    constructor(props) {
        super(props);

        this.createRows = this.createRows.bind(this);
    }

    createRows(donations) {

        let donationsSorted = _.sortBy(donations, donation => {
            return Date(donation.created_date);
        });

        donationsSorted = donationsSorted.reverse();
        const latestDonations = donationsSorted.slice(0,ROWS_TO_SHOW);

        const result = _.map(latestDonations, donation => {
            return( <StyledTableRow>
                    <TableCell>{donation.close_date}</TableCell>
                    <TableCell>${donation.amount}</TableCell>
                    <TableCell>{donation.type}</TableCell>
                </StyledTableRow>);
        });

        return result;
    }

    render() {
        return (
            <Container className={styles.donations} >
                <Typography className={styles.donations_title} gutterBottom='true' variant='h4'>Financial Support Activity(Top 3)</Typography>
                <TableContainer className="main_table_container" style={{"marginTop":"1em"}} component={Paper} variant='outlined'>
                    <Table className="main_table">
                        <TableHead>
                            <TableRow>
                                <StyledTableCell>Date of Donation</StyledTableCell>
                                <StyledTableCell>Amount</StyledTableCell>
                                <StyledTableCell>Campaign Type</StyledTableCell>
                            </TableRow>
                        </TableHead>
                        <TableBody>
                            { this.props.donations && this.createRows(this.props.donations) }
                        </TableBody>
                    </Table>
                </TableContainer>
            </Container>
        );
    }
}


export default Donations;