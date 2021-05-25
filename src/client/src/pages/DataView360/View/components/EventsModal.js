import React, { Component, Fragment } from 'react';
import {
    Paper,
    Table,
    TableContainer,
    TableHead,
    TableBody,
    TableRow,
    TableCell,
} from '@material-ui/core';
import { withStyles } from '@material-ui/core/styles';
import _ from 'lodash';


const customStyles = theme => ({
    spaceIcon: {
        marginTop: 3,
        marginRight: 3
    },
    headerCell: {
        fontWeight: "bold",
    },
    paper: {
        position: 'absolute',
        width: 400,
        backgroundColor: theme.palette.background.paper,
        border: '2px solid #000',
        boxShadow: theme.shadows[5],
        padding: theme.spacing(2, 4, 3),
    }
});

class EventsModal extends Component {

    render() {

        return (
            <Fragment>
                <TableContainer component={Paper} style={{ "marginBottom": "1em" }} variant='outlined'>
                    <Table>
                        <TableHead>
                            <TableRow>
                                <TableCell align="center">Subtype</TableCell>
                                <TableCell align="center">Time</TableCell>
                                <TableCell align="center">Type</TableCell>
                                <TableCell align="center">User</TableCell>
                            </TableRow>
                        </TableHead>
                        <TableBody>
                            {_.map(this.props.data, (adoptionInfo, index) => {
                                return <TableRow key={index}>
                                    <TableCell align="center">{adoptionInfo["Subtype"]}</TableCell>
                                    <TableCell align="center">{adoptionInfo["Time"]}</TableCell>
                                    <TableCell align="center">{adoptionInfo["Type"]}</TableCell>
                                    <TableCell align="center">{adoptionInfo["User"]}</TableCell>
                                </TableRow>
                            })}
                        </TableBody>
                    </Table>
                </TableContainer>
            </Fragment>)
    }
}

export default withStyles(customStyles)(EventsModal);