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
import { withStyles } from '@material-ui/core/styles';
import _ from 'lodash';
import moment from 'moment';
import TimelineIcon from '@material-ui/icons/Timeline';
import DataTableHeader from './DataTableHeader';

const customStyles = theme => ({
    spaceIcon: {
        marginTop: 3,
        marginRight: 3
    },
    headerCell: {
        fontWeight: "bold"
    },
});

const SHIFTS_TO_SHOW = 3;

class VolunteerHistory extends Component {

    createShiftRows(shifts) {
        const shiftsSorted = _.sortBy(shifts, shift => {
            return new moment(shift.from);
        }).reverse();

        const lastShifts = shiftsSorted.slice(0, SHIFTS_TO_SHOW)
        const result = _.map(lastShifts, (shift, index) => {
            shift.from = (shift.from === "Invalid date") ? "Unknown" : moment(shift.from).format("MM-DD-YYYY")
            return(<TableRow key={index}>
                    <TableCell>{shift.from}</TableCell>
                    <TableCell>{shift.assignment}</TableCell>
                </TableRow>);

        });

        return result;
    }

    render() {
        const {classes} = this.props;

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
                                    <TableCell className={classes.headerCell}>Date</TableCell>
                                    <TableCell className={classes.headerCell}>Assignment</TableCell>
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


export default withStyles(customStyles)(VolunteerHistory);