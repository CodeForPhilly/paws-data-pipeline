import React, {Component} from 'react';
import {Box, Divider, Paper, Typography} from '@material-ui/core';
import PhoneIcon from '@material-ui/icons/Phone';
import MailOutlineIcon from '@material-ui/icons/MailOutline';
import HomeIcon from '@material-ui/icons/Home';

import _ from 'lodash';
import {formatPhoneNumber} from "../../../../utils/utils";
import Grid from "@material-ui/core/Grid";


const SOURCE_TYPES = ["salesforcecontacts", "volgistics", "shelterluvpeople"]


class ContactInfo extends Component {

    populate_participant_with_data_source(participant, participantData) {
        return {
            first_name: _.get(participantData, "first_name") || _.get(participant, "first_name") || "",
            last_name: _.get(participantData, "last_name") || _.get(participant, "last_name") || "",
            email: _.get(participantData, "email") || _.get(participant, "email") || "",
            mobile: _.get(participantData, "mobile") || _.get(participant, "mobile") || "",
            city: _.get(participantData, "city") || _.get(participant, "city") || "",
            street_and_number: _.get(participantData, "street_and_number") || _.get(participant, "street_and_number") || "",
            zip: _.get(participantData, "zip") || _.get(participant, "zip") || "",
            state: _.get(participantData, "state") || _.get(participant, "state") || ""
        };
    }

    //populates by the order of the source types array
    populate_participant_data(participantArray) {
        let retVal = {};

        _.map(SOURCE_TYPES, source_type => {
            const participant_source_data = _.find(participantArray, {"source_type": source_type});
            retVal = this.populate_participant_with_data_source(participant_source_data, retVal);
        });

        return retVal
    }


    render() {
        let participantArray = _.get(this.props, "participant");
        let participantData = this.populate_participant_data(participantArray);
        let {
            first_name: firstName,
            last_name: lastName,
            mobile,
            email,
            city,
            state,
            zip,
            street_and_number: streetAndNumber,
        } = participantData

        return (
            <Paper elevation={2} style={{padding: '2em'}}>
                <Grid container direction={'column'} spacing={1}>
                    <Grid item>
                        <Box display="flex" justifyContent="center">
                            <Typography
                                variant={'h6'}>{firstName + ' ' + lastName}
                            </Typography>
                        </Box>
                        <Box pb={2}>
                            <Divider/>
                        </Box>
                    </Grid>
                    {mobile && (
                        <Grid container item direction={'row'} spacing={1} alignItems="center">
                            <Grid item>
                                <PhoneIcon color='primary' fontSize='small'/>
                            </Grid>
                            <Grid item>
                                <Typography variant={'body2'}>{formatPhoneNumber(mobile)}
                                </Typography>
                            </Grid>
                        </Grid>
                    )}
                    {email && (
                        <Grid container item direction={'row'} spacing={1} alignItems="center">
                            <Grid item>
                                <MailOutlineIcon color='primary' fontSize='small'/>
                            </Grid>
                            <Grid item>
                                <Typography variant={'body2'}>
                                    {email}
                                </Typography>
                            </Grid>
                        </Grid>
                    )}
                    {(city || state || zip || streetAndNumber) && (
                        <Grid container item direction={'column'} alignItems="flex-start">
                            {streetAndNumber && (
                                <Grid container item direction="row" alignItems="center" spacing={1}>
                                    <Grid item>
                                        <HomeIcon color='primary' fontSize='small'/>
                                    </Grid>
                                    <Grid item>
                                        <Typography variant={'body2'}>
                                            {streetAndNumber}
                                        </Typography>
                                    </Grid>
                                </Grid>
                            )}
                            <Grid container item direction="row" spacing={1} style={{paddingLeft: 37}}>
                                <Grid item>
                                    <Typography variant={'body2'}>
                                        {`
                                            ${city ? city + ", " : ""}
                                            ${state ? state + " " : ""}
                                            ${zip ? zip : ""}
                                        `}
                                    </Typography>
                                </Grid>
                            </Grid>
                        </Grid>
                    )}
                </Grid>

            </Paper>
        );
    }
}

export default ContactInfo;