import React, { Component } from 'react';
import {
    Paper,
    Container,
    IconButton
} from '@material-ui/core';
import LinkIcon from '@material-ui/icons/Link';
import _ from 'lodash';
import Grid from "@material-ui/core/Grid";
import PetsIcon from "@material-ui/icons/Pets";

import CollapsibleTable from './CollapsibleTable';
import DataTableHeader from './DataTableHeader';


const PET_COUNT = 5;

class AnimalInfo extends Component {

    getLatestPets(petObject, events) {

        function customizer(objValue, srcValue) {
            if (_.isObject(objValue) && _.isObject(srcValue)) {
                // sort according to date of most recent event
                return _.set(objValue, 'Events', _.orderBy(srcValue, ['Time'], ['desc']));
            }
        }

        let result = _.mergeWith(petObject, events, customizer);
        let nonEmptyEvents = _.filter(result, function(pet) { return pet["Events"] && _.size(pet["Events"]) > 0 });
        result = [..._.orderBy(nonEmptyEvents, ['Events[0].Time'], ['desc'])]
        return result.slice(0, PET_COUNT);
    }

    render() {
        const numOfPets = _.size(this.props.pets);
        const events = this.props.events;
        const latestPets = this.getLatestPets(this.props.pets, events);
        const headerText = this.props.headerText;
        const headerAddition = (numOfPets > PET_COUNT) ? " (Showing " + PET_COUNT + " Pets out of " + numOfPets + ")" : ""
        const shelterLuvPersonURL = `https://www.shelterluv.com/phlp-p-${this.props.shelterluv_id}`;

        return (
            <Container component={Paper} style={{ "marginTop": "1em" }}>
                <DataTableHeader headerText={headerText + headerAddition}
                    emojiIcon={<PetsIcon color='primary' fontSize='inherit'/>}
                >
                    <Grid item>
                        <IconButton style={{ 'padding': 0, 'paddingLeft': 5 }} color="primary" aria-label="link" href={shelterLuvPersonURL} target="_blank">
                            <LinkIcon />
                        </IconButton>
                    </Grid>
                </DataTableHeader>
                <CollapsibleTable data={latestPets} events={events} />
            </Container>
        );
    }
}


export default AnimalInfo;