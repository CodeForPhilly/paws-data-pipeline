import React, {Component} from 'react';
import {Paper, Typography, Container} from '@material-ui/core';
import {withStyles} from '@material-ui/core/styles';
import styles from "./styles/ContactInfo.module.css";
import _ from 'lodash';
import {formatPhoneNumber} from "../../../utils/utils";


const SOURCE_TYPES = ["salesforcecontacts", "volgistics", "shelterluvpeople"]
const StyledContact = withStyles((theme) => ({
    root: {
        span: {
            fontWeight: 600,
        },
    }
}))(Typography);


class ContactInfo extends Component {
    constructor(props) {
        super(props);
    }


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
        let participantArray = _.get(this.props, "participant");
        let participantData = this.populate_participant_data(participantArray);

        return (
            <Container className={styles.contact_info}>
                <Paper variant='outlined' className={styles.contact_info_main} style={{padding: '1em'}}>
                    <div className={styles.contact_container}>
                        <Typography className={styles.contact_info_name}>
                            <span>
                                {participantData.first_name}{'\t'}
                                {participantData.last_name}
                            </span>
                        </Typography>
                        <StyledContact className={styles.contact_info_phone}>
                            <span>
                                {formatPhoneNumber(participantData.mobile)}
                            </span>
                        </StyledContact>
                        <Typography className={styles.contact_info_email}>
                            <span>
                                {participantData.email}
                            </span>
                        </Typography>
                        <Typography className={styles.contact_info_address}>
                            <span style={{"textTransform": "uppercase"}}>
                                {participantData.street_and_number}{'\t'}
                                {participantData.city}{'\t'}
                            </span>
                        </Typography>
                    </div>
                </Paper>
            </Container>
        );
    }
}


export default ContactInfo;