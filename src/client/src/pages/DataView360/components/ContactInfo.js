import React, { Component } from 'react';
import { Paper, Typography, Container} from '@material-ui/core';
import { withStyles } from '@material-ui/core/styles';
import styles from "./styles/ContactInfo.module.css";

import _ from 'lodash';

const StyledContact = withStyles((theme)=>({
    root:{
        span:{
        fontWeight:600,
        },
    },

}))(Typography);

class ContactInfo extends Component {
    render() {
        const participantArray = _.get(this.props, "participant")
        const participant = participantArray[0]
        const phoneStr = participant.mobile;
        let phone = _.isEmpty(phoneStr) ? '-' : phoneStr.split(" ").join("");
        return (<Container className={styles.contact_info}>
                <Paper variant='outlined' className={styles.contact_info_main} style={{padding:'1em'}}>
                    <div className={styles.contact_container}>
                        <Typography className={styles.contact_info_name}>
                            <span>
                                {participant.first_name}{'\t'}
                                {participant.last_name}
                            </span>
                        </Typography>
                        <StyledContact className={styles.contact_info_phone}>
                            <span>
                                {phone}
                            </span>
                        </StyledContact>
                        <Typography className={styles.contact_info_email}>
                            <span>
                                {participant.email}
                            </span>
                        </Typography>
                        <Typography className={styles.contact_info_address}>
                            <span style={{"textTransform":"uppercase"}}>
                                {participant.street_and_number}{'\t'}
                                {participant.city}{'\t'}
                            </span>
                        </Typography>
                    </div>
                </Paper>
            </Container>
        );
    }
}


export default ContactInfo;