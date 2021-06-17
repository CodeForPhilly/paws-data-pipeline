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
import { withStyles } from '@material-ui/core/styles';
import _ from 'lodash';
import moment from "moment";
import Grid from "@material-ui/core/Grid";
import PetsIcon from "@material-ui/icons/Pets";
import DataTableHeader from './DataTableHeader';
import { showAnimalAge } from '../../../../utils/utils'


const customStyles = theme => ({
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

const PET_COUNT = 3;

class Adoptions extends Component {

    getLatestPets(animals) {
        const latestPets = _.sortBy(animals, animal => {
            return animal.Events.Time
        }).reverse()

        return latestPets.slice(0, PET_COUNT)
    }

    createRows(data) {
        const result = _.map(data, (row, index) => {
            const photo = row.Photos[0]
            return (
                <TableRow key={index}>
                    <TableCell align="center">{row.Name}</TableCell>
                    <TableCell align="center">{row.Type}</TableCell>
                    <TableCell align="center">{moment.unix(row.Events.Time).format("DD MMM YYYY")}</TableCell>
                    <TableCell align="center">{showAnimalAge(row.DOBUnixTime)}</TableCell>
                    <TableCell align="center">{<img src={photo} alt="animal" style={{ "maxWidth": "100px" }} />}</TableCell>
                </TableRow>
            );
        });

        return result;
    }

    combineAnimalAndEvents(animals, events) {
        let combined = {}
        for (const id in animals) {
            if (_.includes(_.keys(events), id)) {
                combined[id] = { ...animals[id], "Events": events[id][0] }
            }
        }
        return combined
    }

    render() {
        const { pets, events, headerText } = this.props;
        const combined = this.combineAnimalAndEvents(pets, events)

        const numOfPets = _.size(combined);
        const latestPets = this.getLatestPets(combined);

        const headerAddition = (numOfPets > PET_COUNT) ? " (Most Recent " + PET_COUNT + ")" : ""

        return (
            <Container component={Paper} style={{ "marginTop": "1em" }}>
                <DataTableHeader
                    headerText={headerText + headerAddition}
                    emojiIcon={<PetsIcon color='primary' fontSize='inherit' />}
                >
                    <Grid item>
                        <IconButton style={{ 'padding': 0, 'paddingLeft': 5 }} color="primary" aria-label="link" href={""}>
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
                                <TableCell align="center">Adoption Date</TableCell>
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


export default withStyles(customStyles)(Adoptions);