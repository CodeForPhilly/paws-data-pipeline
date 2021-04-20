import React, { Component } from 'react';
import {
    Paper,
    Typography,
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
import Grid from "@material-ui/core/Grid";
import EmojiPeopleIcon from '@material-ui/icons/EmojiPeople';
import TimelineIcon from '@material-ui/icons/Timeline';

const customStyles = theme => ({
    spaceIcon: {
        marginTop: 3,
        marginRight: 3
    },
    headerCell: {
        fontWeight: "bold"
    },
});

const SHIFTS_TO_SHOW = 5;

class Volunteer extends Component {

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
                    <Typography variant='h5'>
                        <Grid container style={{"margin": "0.5em"}} direction={'row'}>
                            <Grid item className={classes.spaceIcon}>
                                <EmojiPeopleIcon color='primary' fontSize='inherit'/>
                            </Grid>
                            <Grid item>
                                Volunteer Activity
                            </Grid>
                        </Grid>
                    </Typography>
                    <TableContainer component={Paper} style={{"marginBottom": "1em"}} variant='outlined'>
                        <Table>
                            <TableHead>
                                <TableRow>
                                    <TableCell className={classes.headerCell}>Volunteer activity start</TableCell>
                                    <TableCell className={classes.headerCell}>Life hours</TableCell>
                                    <TableCell className={classes.headerCell}>YTD hours</TableCell>
                                </TableRow>
                            </TableHead>
                            <TableBody>
                                { this.props.volunteer && (
                                <TableRow>
                                    <TableCell>{moment(this.props.volunteer.start_date).format("MM-DD-YYYY")}</TableCell>
                                    <TableCell>{this.props.volunteer.life_hours.toFixed(2)}</TableCell>
                                    <TableCell>{this.props.volunteer.ytd_hours.toFixed(2)}</TableCell>
                                </TableRow>
                                )}
                            </TableBody>
                        </Table>
                    </TableContainer>
                </Container>
                <Container component={Paper} style={{"marginTop": "1em"}}>
                    <Typography variant='h5'>
                        <Grid container style={{"margin": "0.5em"}} direction={'row'}>
                            <Grid item className={classes.spaceIcon}>
                                <TimelineIcon color='primary' fontSize='inherit'/>
                            </Grid>
                            <Grid item>
                                Volunteer History (Top 5)
                            </Grid>
                        </Grid>
                    </Typography>
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


export default withStyles(customStyles)(Volunteer);