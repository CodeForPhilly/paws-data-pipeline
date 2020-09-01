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

class Volunteer extends Component {
    render() {

        return (
            <Container style={{"marginTop":"1em"}}>
                <Typography align='center' gutterBottom='true' variant='h4'>Volunteer Records</Typography>
                <TableContainer style={{"marginTop":"1em"}} component={Paper} variant='outlined'>
                    <Table>
                        <TableHead>
                            <TableRow>
                                <StyledTableCell align="center">Volunteer activity start</StyledTableCell>
                                <StyledTableCell align="center">Life hours</StyledTableCell>
                                <StyledTableCell align="center">YTD hours</StyledTableCell>
                            </TableRow>
                        </TableHead>
                        <TableBody>
                            { this.props.volunteer && (
                            <StyledTableRow>
                                <TableCell align="center">{this.props.volunteer.start_date}</TableCell>
                                <TableCell align="center">{this.props.volunteer.life_hours}</TableCell>
                                <TableCell align="center">{this.props.volunteer.ytd_hours}</TableCell>
                            </StyledTableRow>
                            )}
                        </TableBody>
                    </Table>
                </TableContainer>
            </Container>
        );
    }
}


export default Volunteer;