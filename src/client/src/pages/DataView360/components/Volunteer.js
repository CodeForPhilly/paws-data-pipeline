import React, { Component } from 'react';
import { Paper, Typography, Table, TableContainer, TableHead, TableBody, TableRow, TableCell, Container} from '@material-ui/core';
import { withStyles } from '@material-ui/core/styles';
import styles from "./styles/Volunteer.module.css";
import "./styles/table.css";
import _ from 'lodash';
import moment from 'moment';

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

const SHIFTS_TO_SHOW = 3;

class Volunteer extends Component {

    createShiftRows(shifts) {
        const shiftsSorted = _.sortBy(shifts, shift => {
            return new Date(shift.from).getTime();
        });

        const lastShifts = shiftsSorted.slice(shiftsSorted.length - SHIFTS_TO_SHOW, shiftsSorted.length)

        const result = _.map(lastShifts, (shift, index) => {
            return(<StyledTableRow key={index}>
                    <TableCell>{moment(shift.from).format("YYYY-MM-DD")}</TableCell>
                    <TableCell>{shift.assignment}</TableCell>
                </StyledTableRow>);

        });

        return result;
    }

    render() {

        return (
            <React.Fragment>
                <Container className={styles.volunteer_activity} style={{"marginTop":"1em"}}>
                    <Typography className={styles.volunteer_activity_title} variant='h4'>Volunteer Activity</Typography>
                    <TableContainer className="main_table_container" style={{"marginTop":"1em"}} component={Paper}>
                        <Table className="main_table">
                            <TableHead>
                                <TableRow>
                                    <StyledTableCell>Volunteer activity start</StyledTableCell>
                                    <StyledTableCell>Life hours</StyledTableCell>
                                    <StyledTableCell>YTD hours</StyledTableCell>
                                </TableRow>
                            </TableHead>
                            <TableBody>
                                { this.props.volunteer && (
                                <StyledTableRow>
                                    <TableCell>{this.props.volunteer.start_date}</TableCell>
                                    <TableCell>{this.props.volunteer.life_hours}</TableCell>
                                    <TableCell>{this.props.volunteer.ytd_hours}</TableCell>
                                </StyledTableRow>
                                )}
                            </TableBody>
                        </Table>
                    </TableContainer>
                </Container>
                <Container className={styles.volunteer_history} style={{"marginTop":"1em"}}>
                    <Typography className={styles.volunteer_history_title} variant='h4'>Volunteer History (Top 3)</Typography>
                    <TableContainer className="main_table_container" style={{"marginTop":"1em"}} component={Paper} variant='outlined'>
                        <Table className="main_table">
                            <TableHead>
                                <TableRow>
                                    <StyledTableCell>Date</StyledTableCell>
                                    <StyledTableCell>Assignment</StyledTableCell>
                                </TableRow>
                            </TableHead>
                            <TableBody>
                                { this.props.volunteerShifts &&  this.createShiftRows(this.props.volunteerShifts) }
                            </TableBody>
                        </Table>
                    </TableContainer>
                </Container>
            </React.Fragment>
        );
    }
}


export default Volunteer;