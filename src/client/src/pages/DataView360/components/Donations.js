import React, { Component } from 'react';
import { Paper, Typography, Table, TableContainer, TableHead, TableBody, TableRow, TableCell, Container} from '@material-ui/core';
import { withStyles } from '@material-ui/core/styles';
import "./styles/Donations.css";
import _ from 'lodash';


const StyledTableCell = withStyles((theme)=>({
    head:{
        backgroundColor: theme.palette.grey.A100,
        fontWeight: 600,
    }
}))(TableCell);

const StyledTableRow = withStyles((theme)=>({
    root:{
        '&:nth-of-type(even)':{
            backgroundColor: theme.palette.action.hover,
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

        const result = _.map(latestDonations, (donation, index) => {
            return( <StyledTableRow key={index}>
                    <TableCell align="center">{donation.close_date}</TableCell>
                    <TableCell align="center">${donation.amount}</TableCell>
                    <TableCell align="center">{donation.type}</TableCell>
                </StyledTableRow>);
        });

        return result;
    }

    render() {
        return (
            <Container style={{"marginTop":"1em"}}>
                <Typography align='center' variant='h4'>Financial Support Activity(Top 3)</Typography>
                <TableContainer style={{"marginTop":"1em"}} component={Paper} variant='outlined'>
                    <Table>
                        <TableHead>
                            <TableRow>
                                <StyledTableCell align="center">Date of Donation</StyledTableCell>
                                <StyledTableCell align="center">Amount</StyledTableCell>
                                <StyledTableCell align="center">Campaign Type</StyledTableCell>
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