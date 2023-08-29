import React, { Component } from 'react';
import {
    IconButton,
    Paper,
    Table,
    TableContainer,
    TableHead,
    TableBody,
    TableRow,
    TableCell,
    Container
} from '@material-ui/core';
import LinkIcon from '@material-ui/icons/Link';
import _ from 'lodash';
import moment from "moment-timezone";
import Grid from "@material-ui/core/Grid";
import PetsIcon from "@material-ui/icons/Pets";

import DataTableHeader from './DataTableHeader';
import { showAnimalAge } from '../../../../utils/utils'

const PET_COUNT = 3;

class Fosters extends Component {

    getLatestPets(animals) {
        const latestPets = _.sortBy(animals, animal => {
            return animal.Events.Time
        }).reverse()

        return latestPets.slice(0, PET_COUNT)
    }

    combineAnimalAndEvents(animals, events) {
        let combined = {}
        for (const id in animals) {
            if (_.includes(_.keys(events), id)) {
                let sortedEvents = _.sortBy(events[id], ['Time'])
                combined[id] = { ...animals[id], "Events": sortedEvents }
            }
        }
        return combined
    }

    createRows(data) {
        const result = _.map(data, (row, index) => {
            const photo = row.Photos[0]
            return (
                <TableRow key={index}>
                    <TableCell align="center">{row.Name}</TableCell>
                    <TableCell align="center">{row.Type}</TableCell>
                    <TableCell align="center">{moment.unix(row.Events[0].Time).format("DD MMM YYYY")}</TableCell>
                    <TableCell align="center">{moment.unix(row.Events[1].Time).format("DD MMM YYYY")}</TableCell>
                    <TableCell align="center">{showAnimalAge(row.DOBUnixTime)}</TableCell>
                    <TableCell align="center">{<img src={photo} alt="animal" style={{ "maxWidth": "100px" }} />}</TableCell>
                </TableRow>
            );
        });

        return result;
    }

    render() {
        const { pets, events, headerText, shelterluvShortId } = this.props;
        const combined = this.combineAnimalAndEvents(pets, events)
        const numOfPets = _.size(combined);
        const latestPets = this.getLatestPets(combined);
        const headerAddition = (numOfPets > PET_COUNT) ? " (Most Recent " + PET_COUNT + ")" : ""
        const shelterLuvPersonURL = `https://www.shelterluv.com/phlp-p-${shelterluvShortId}`;

        return (
            <Container component={Paper} style={{ "marginTop": "1em" }}>
                <DataTableHeader
                    headerText={headerText + headerAddition}
                    emojiIcon={<PetsIcon color='primary' fontSize='inherit' />}
                >
                    <Grid item>
                        <IconButton style={{ 'padding': 0, 'paddingLeft': 5 }} color="primary" aria-label="link" href={shelterLuvPersonURL} target="_blank">
                            <LinkIcon />
                        </IconButton>
                    </Grid>
                </DataTableHeader>
                <TableContainer component={Paper} style={{ "marginBottom": "1em" }}>
                    <Table>
                        <TableHead>
                            <TableRow>
                                <TableCell align="center">Name</TableCell>
                                <TableCell align="center">Animal Type</TableCell>
                                <TableCell align="center">Start Date</TableCell>
                                <TableCell align="center">End Date</TableCell>
                                <TableCell align="center">Age</TableCell>
                                <TableCell align="center">Photo</TableCell>
                            </TableRow>
                        </TableHead>
                        <TableBody>
                            {latestPets && this.createRows(latestPets)}
                        </TableBody>
                    </Table>
                </TableContainer>
            </Container>
        );
    }
}


export default Fosters;