import React, { Component } from 'react';
import {
    Paper,
    Table,
    TableContainer,
    TableHead,
    TableBody,
    TableRow,
    TableCell,
    Container,
} from '@material-ui/core';
import _ from 'lodash';
import moment from 'moment';
import TimelineIcon from '@material-ui/icons/Timeline';
import DataTableHeader from './DataTableHeader';


const SHIFTS_TO_SHOW = 3;

class VolunteerHistory extends Component {

    createShiftRows(shifts) {
        const shiftsFiltered = _.filter(shifts, function(s) { return s.from !== "Invalid date"});
        const shiftsSorted = _.sortBy(shiftsFiltered, shift => {
            return new moment(shift.from).format("YYYY-MM-DD");
        }).reverse();

        const lastShifts = shiftsSorted.slice(0, SHIFTS_TO_SHOW)
        
        const result = _.map(lastShifts, (shift, index) => {
            shift.from = moment(shift.from).format("YYYY-MM-DD")
            return(<TableRow key={index}>
                    <TableCell>{shift.from}</TableCell>
                    <TableCell>{shift.assignment}</TableCell>
                </TableRow>);

        });

        return result;
    }

    render() {

        return (
            <React.Fragment>
                <Container component={Paper} style={{"marginTop": "1em"}}>
                    <DataTableHeader headerText={`Volunteer History (Most Recent ${SHIFTS_TO_SHOW})`} 
                        emojiIcon={<TimelineIcon color='primary' fontSize='inherit'/>}
                    />
                    <TableContainer component={Paper} style={{"marginBottom":"1em"}} variant='outlined'>
                        <Table>
                            <TableHead>
                                <TableRow>
                                    <TableCell>Date</TableCell>
                                    <TableCell>Assignment</TableCell>
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


export default VolunteerHistory;