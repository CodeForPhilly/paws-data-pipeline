import React, { Component } from 'react';
import { Paper, Typography, Table, TableContainer, TableHead, TableBody, TableRow, TableCell, Container} from '@material-ui/core';
import { withStyles } from '@material-ui/core/styles';

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

class Donations extends Component {
    constructor(props) {
        super(props);

        this.createRow = this.createRow.bind(this);
    }

    createRow(item) {
        return( <StyledTableRow>
                    <TableCell align="center">{item.date}</TableCell>
                    <TableCell align="center">{item.amount}</TableCell>
                    <TableCell align="center">{item.type}</TableCell>
                </StyledTableRow>);
    }

    render() {
        return (
            <Container style={{"marginTop":"1em"}}>
                <Typography align='center' gutterBottom='true' variant='h4'>Donation Records</Typography>
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
                            { this.props.donations && this.props.donations.map(i => this.createRow(i)) }
                        </TableBody>
                    </Table>
                </TableContainer>
            </Container>
        );
    }
}


export default Donations;