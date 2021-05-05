import React from 'react';
import PropTypes from 'prop-types';
import { makeStyles } from '@material-ui/core/styles';
import Box from '@material-ui/core/Box';
import Collapse from '@material-ui/core/Collapse';
import IconButton from '@material-ui/core/IconButton';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableContainer from '@material-ui/core/TableContainer';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import Typography from '@material-ui/core/Typography';
import Paper from '@material-ui/core/Paper';
import KeyboardArrowDownIcon from '@material-ui/icons/KeyboardArrowDown';
import KeyboardArrowUpIcon from '@material-ui/icons/KeyboardArrowUp';

import _ from 'lodash';
import moment from "moment";

const useRowStyles = makeStyles({
    root: {
        '& > *': {
            borderBottom: 'unset',
        },
    },
});

function getAnimalAge(epochTime) {
    let dateOfBirth = moment(epochTime * 1000);
    return moment().diff(dateOfBirth, 'years');
}

function Row(props) {
    const [open, setOpen] = React.useState(false);
    const classes = useRowStyles();
    const { row, events } = props;
    return (
        <React.Fragment>
            <TableRow className={classes.root}>
                <TableCell>
                    <IconButton aria-label="expand row" size="small" onClick={() => setOpen(!open)}>
                        {open ? <KeyboardArrowUpIcon /> : <KeyboardArrowDownIcon />}
                    </IconButton>
                </TableCell>
                <TableCell component="th" scope="row">
                    {row.Name}
                </TableCell>
                <TableCell align="center">{row.Type}</TableCell>
                <TableCell align="center">{row.Breed}</TableCell>
                <TableCell align="center">{getAnimalAge(row.DOBUnixTime)}</TableCell>
                <TableCell align="center">{<img src={row.Photos[0]} alt="animal" style={{ "maxWidth": "100px" }} />}</TableCell>
            </TableRow>
            <TableRow>
                <TableCell style={{ paddingBottom: 0, paddingTop: 0 }} colSpan={6}>
                    <Collapse in={open} timeout="auto" unmountOnExit>
                        <Box margin={1}>
                            <Typography variant="h6" gutterBottom component="div">
                                History
                            </Typography>
                            <Table size="small" aria-label="purchases">
                                <TableHead>
                                    <TableRow>
                                        <TableCell align="center">Subtype</TableCell>
                                        <TableCell align="center">Time</TableCell>
                                        <TableCell align="center">Type</TableCell>
                                        <TableCell align="center">User</TableCell>
                                    </TableRow>
                                </TableHead>
                                <TableBody>
                                    {events.map((historyRow) => (
                                        <TableRow key={historyRow.Time}>
                                            <TableCell component="th" scope="row">
                                                {historyRow.Subtype}
                                            </TableCell>
                                            <TableCell align="center">{moment.unix(historyRow.Time).format("DD MMM YYYY")}</TableCell>
                                            <TableCell align="center">{historyRow.Type}</TableCell>
                                            <TableCell align="center">{historyRow.User}</TableCell>
                                        </TableRow>
                                    ))}
                                </TableBody>
                            </Table>
                        </Box>
                    </Collapse>
                </TableCell>
            </TableRow>
        </React.Fragment>
    );
}

export default function CollapsibleTable(props) {
    const data = props.data;
    let events = props.events;
    const rows = _.values(data)
    return (
        <TableContainer component={Paper} style={{"marginBottom": "1em"}}>
            <Table aria-label="collapsible table">
                <TableHead>
                    <TableRow>
                        <TableCell />
                        <TableCell align="center">Name</TableCell>
                        <TableCell align="center">Animal Type</TableCell>
                        <TableCell align="center">Breed</TableCell>
                        <TableCell align="center">Age</TableCell>
                        <TableCell align="center">Photo</TableCell>
                    </TableRow>
                </TableHead>
                <TableBody>
                    {rows.map((row) => {
                        const eventsData = events[row["Internal-ID"]];
                        return (eventsData && <Row key={row["Internal-ID"]} row={row} events={eventsData}/>)
                    })}
                </TableBody>
            </Table>
        </TableContainer>
    );
}