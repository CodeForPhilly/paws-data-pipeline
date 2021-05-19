import React, { Component } from 'react';
import {
    Paper,
    Typography,
    Container,
    IconButton
} from '@material-ui/core';
import LinkIcon from '@material-ui/icons/Link';
import { withStyles } from '@material-ui/core/styles';
import _ from 'lodash';
import moment from "moment";
import Grid from "@material-ui/core/Grid";
import PetsIcon from "@material-ui/icons/Pets";

import CollapsibleTable from './CollapsibleTable';
import DataTableHeader from './DataTableHeader';


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

const PET_COUNT = 5;

class Adoptions extends Component {

    getLatestPets(petObject) {
        return petObject;
    }

    render() {
        const { classes } = this.props;
        const numOfPets = _.size(this.props.adoptions);
        const latestPets = this.getLatestPets(this.props.adoptions);

        const events = this.props.events;
        const headerText = "Adoption Records"
        const headerAddition = (numOfPets > PET_COUNT) ? " (Showing " + PET_COUNT + " Pets out of " + numOfPets + ")" : ""

        return (
            <Container component={Paper} style={{ "marginTop": "1em" }}>
                <DataTableHeader
                    headerText={headerText + headerAddition}
                    emojiIcon={<PetsIcon color='primary' fontSize='inherit' />}
                >
                    <Grid item>
                        <IconButton style={{ 'padding': 0, 'paddingLeft': 5 }} color="primary" aria-label="link" href={shelterLuvPersonURL}>
                            <LinkIcon />
                        </IconButton>
                    </Grid>
                </DataTableHeader>
                <CollapsibleTable data={latestPets} events={events} />
            </Container>
        );
    }
}


export default withStyles(customStyles)(Adoptions);