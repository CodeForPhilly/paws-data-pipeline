import React, { Component } from 'react';
import { Paper, Typography, Table, TableContainer, TableHead, TableBody, TableRow, TableCell, Container} from '@material-ui/core';
import { withStyles } from '@material-ui/core/styles';
import "./styles/Volunteer.css";
import _ from 'lodash';
import moment from 'moment';


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

const SHIFTS_TO_SHOW = 3;

class Volunteer extends Component {
    constructor(props) {
        super(props);
    }

    createShiftRows(shifts) {
        const shiftsSorted = _.sortBy(shifts, shift => {
            return new Date(shift.from).getTime();
        });

        const lastShifts = shiftsSorted.slice(shiftsSorted.length - SHIFTS_TO_SHOW, shiftsSorted.length)

        const result = _.map(lastShifts, shift => {
            return(<StyledTableRow>
                    <TableCell align="center">{moment(shift.from).format("YYYY-MM-DD")}</TableCell>
                    <TableCell align="center">{shift.assignment}</TableCell>
                </StyledTableRow>);

        });

        return result;
    }

    render() {

        return (
            <div>
                <Container style={{"marginTop":"1em"}}>
                    <Typography align='center' gutterBottom='true' variant='h4'>Volunteer Activity</Typography>
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

                <Container style={{"marginTop":"1em"}}>
                    <Typography align='center' gutterBottom='true' variant='h4'>Volunteer History(Top 3)</Typography>
                    <TableContainer style={{"marginTop":"1em"}} component={Paper} variant='outlined'>
                        <Table>
                            <TableHead>
                                <TableRow>
                                    <StyledTableCell align="center">Date</StyledTableCell>
                                    <StyledTableCell align="center">Assignment</StyledTableCell>
                                </TableRow>
                            </TableHead>
                            <TableBody>
                                { this.props.volunteerShifts &&  this.createShiftRows(this.props.volunteerShifts) }
                            </TableBody>
                        </Table>
                    </TableContainer>
                </Container>
            </div>
        );
    }
}


export default Volunteer;