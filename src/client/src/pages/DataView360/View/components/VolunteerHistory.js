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
    headerCell: {
        fontWeight: "bold"
    },
});

const SHIFTS_TO_SHOW = 5;

class VolunteerHistory extends Component {

    createShiftRows(shifts) {
        const shiftsSorted = _.sortBy(shifts, shift => {
            return new moment(shift.from);
        }).reverse();

        const lastShifts = shiftsSorted.slice(shiftsSorted.length - SHIFTS_TO_SHOW, shiftsSorted.length)

        const result = _.map(lastShifts, (shift, index) => {
            return(<TableRow key={index}>
                    <TableCell>{moment(shift.from).format("MM-DD-YYYY")}</TableCell>
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
                    <DataTableHeader headerText={"Volunteer History (Top 5)"} 
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