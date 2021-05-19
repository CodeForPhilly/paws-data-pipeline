import React, {Component} from 'react';
import {Box, Container, Divider, Paper, Typography} from '@material-ui/core';
import {withStyles} from '@material-ui/core/styles';
import PhoneIcon from '@material-ui/icons/Phone';
import MailOutlineIcon from '@material-ui/icons/MailOutline';
import HomeIcon from '@material-ui/icons/Home';

import _ from 'lodash';
import {formatPhoneNumber} from "../../../../utils/utils";
import Grid from "@material-ui/core/Grid";


const SOURCE_TYPES = ["salesforcecontacts", "volgistics", "shelterluvpeople"]

const customStyles = theme => ({
    spacingRows: {
        padding: 2
    },
});


class ContactInfo extends Component {

    populate_participant_with_data_source(participant, participantData) {
        return {
            first_name: _.get(participantData, "first_name") || _.get(participant, "first_name"),
            last_name: _.get(participantData, "last_name") || _.get(participant, "last_name"),
            email: _.get(participantData, "email") || _.get(participant, "email"),
            mobile: _.get(participantData, "mobile") || _.get(participant, "mobile"),
            city: _.get(participantData, "city") || _.get(participant, "city"),
            street_and_number: _.get(participantData, "street_and_number") || _.get(participant, "street_and_number")
        };
    }

    //populates by the order of the source types array
    populate_participant_data(participantArray) {
        let retVal = {};

        _.map(SOURCE_TYPES, source_type => {
            const participant_salesforce_data = _.find(participantArray, {"source_type": source_type});
            retVal = this.populate_participant_with_data_source(participant_salesforce_data, retVal);
        });

        return retVal
    }


    render() {
        const {classes} = this.props;

        let participantArray = _.get(this.props, "participant");
        let participantData = this.populate_participant_data(participantArray);

        return (
            <Paper elevation={2} style={{padding: '1em'}}>
                <Container className={classes.containerInfo}>
                    <Grid container direction={'column'}>
                        <Grid container className={classes.spacingRows} direction={'row'} justify='center'>
                            <Grid item>
                                <Typography variant={'h6'}>
                                    <b>{participantData.first_name + ' ' + participantData.last_name}</b>
                                </Typography>
                            </Grid>
                        </Grid>
                        <Box pb={2}>
                            <Divider/>
                        </Box>
                        <Grid container className={classes.spacingRows} direction={'row'} spacing={2}>
                            <Grid item>
                                <PhoneIcon color='secondary' fontSize='inherit'/>
                            </Grid>
                            <Grid item xs={8}>
                                <Typography variant={'body2'}>
                                    {formatPhoneNumber(participantData.mobile)}
                                </Typography>
                            </Grid>
                        </Grid>
                        <Grid container className={classes.spacingRows} direction={'row'} spacing={2}>
                            <Grid item>
                                <MailOutlineIcon color='primary' fontSize='inherit'/>
                            </Grid>
                            <Grid item xs={8}>
                                <Typography variant={'body2'}>
                                    {participantData.email}
                                </Typography>
                            </Grid>
                        </Grid>
                        <Grid container className={classes.spacingRows} direction={'row'} spacing={2}>
                            <Grid item>
                                <HomeIcon color='primary' fontSize='inherit'/>
                            </Grid>
                            <Grid item xs={8}>
                                <Typography variant={'body2'}>
                                    {(participantData.street_and_number + ' ' + participantData.city)}
                                </Typography>
                            </Grid>
                        </Grid>
                    </Grid>
                </Container>

            </Paper>
        );
    }
}


export default withStyles(customStyles)(ContactInfo);