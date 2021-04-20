import React, {Component} from 'react';
import {
    Button,
    Dialog,
    Paper,
    Typography,
    Table,
    TableContainer,
    TableHead,
    TableBody,
    TableRow,
    TableCell,
    Container,
    IconButton
} from '@material-ui/core';
import LinkIcon from '@material-ui/icons/Link';
import {withStyles} from '@material-ui/core/styles';
import _ from 'lodash';
import moment from "moment";
import Grid from "@material-ui/core/Grid";
import PetsIcon from "@material-ui/icons/Pets";

import EventsModal from './EventsModal';


const customStyles = theme => ({
    spaceIcon: {
        marginTop: 3,
        marginRight: 3
    },
    headerCell: {
        fontWeight: "bold",
    }
});

const PET_COUNT = 5;

let modalIsOpen = false;
let modalData = [];

class Fosters extends Component {

    handleOpen(data) {
        modalIsOpen = true;
        modalData = data;
    }

    handleClose() {
        modalIsOpen = false;
        modalData = [];
    }

    getLatestPets(petObject) {
        return petObject;
    }

    getAnimalAge(epochTime) {
        let dateOfBirth = moment(epochTime * 1000);
        return moment().diff(dateOfBirth, 'years');
    }

    render() {
        const {classes} = this.props;
        const numOfPets = _.size(this.props.fosters);
        const latestPets = this.getLatestPets(this.props.fosters);

        return (<Container component={Paper} style={{"marginTop": "1em"}}>
                <Typography variant='h5'>
                    <Grid container style={{"margin": "0.5em"}} direction={'row'}>
                        <Grid item className={classes.spaceIcon}>
                            <PetsIcon color='primary' fontSize='inherit'/>
                        </Grid>
                        <Grid item>
                            Foster Records {(numOfPets > PET_COUNT) && `(Showing ${PET_COUNT} Pets out of " + numOfPets + ")`}
                        </Grid>
                        <Grid item>
                            <IconButton style={{'padding': 0, 'paddingLeft': 5}} color="primary" aria-label="link" component="span">
                                <LinkIcon />
                            </IconButton>
                        </Grid>
                    </Grid>
                </Typography>
                <Dialog
                    open={modalIsOpen}
                    onClose={this.handleClose}
                    aria-labelledby="simple-dialog-title"
                    aria-describedby="simple-dialog-description"
                >
                    <EventsModal data={modalData}/>
                    <Button variant="contained" color="primary" onClick={this.handleClose}>
                        Close
                    </Button>
                </Dialog>
                <TableContainer component={Paper} style={{"marginBottom": "1em"}} variant='outlined'>
                    <Table>
                        <TableHead>
                            <TableRow>
                                <TableCell className={classes.headerCell} align="center">Name</TableCell>
                                <TableCell className={classes.headerCell} align="center">Animal Type</TableCell>
                                <TableCell className={classes.headerCell} align="center">Breed</TableCell>
                                <TableCell className={classes.headerCell} align="center">Age</TableCell>
                                <TableCell className={classes.headerCell} align="center">Photo</TableCell>
                                <TableCell className={classes.headerCell} align="center"></TableCell>
                            </TableRow>
                        </TableHead>
                        <TableBody>
                            {_.map(latestPets, (fosterInfo, index) => {
                                const photoLink = _.get(fosterInfo, "Photos.[0]");
                                const photo = <img src={photoLink} alt="animal" style={{"maxWidth": "100px"}}/>

                                return <TableRow key={index}>
                                    <TableCell align="center">{fosterInfo["Name"]}</TableCell>
                                    <TableCell align="center">{fosterInfo["Type"]}</TableCell>
                                    <TableCell align="center">{fosterInfo["Breed"]}</TableCell>
                                    <TableCell
                                        align="center">{this.getAnimalAge(fosterInfo["DOBUnixTime"])}</TableCell>
                                    <TableCell align="center">{photo}</TableCell>
                                    <TableCell align="center">
                                        <Button variant="contained" color="primary" onClick={() => this.handleOpen(fosterInfo.fosterEvents)}>
                                            More
                                        </Button>
                                    </TableCell>
                                </TableRow>
                            })}
                        </TableBody>
                    </Table>
                </TableContainer>
            </Container>
        );
    }
}


export default withStyles(customStyles)(Fosters);