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
        const phoneStr = _.get(this.props, "participant.phone");
        let phone = _.isEmpty(phoneStr) ? '-' : phoneStr.split(" ").join("");

        return (<Container className={styles.contact_info}>
                <Paper variant='outlined' className={styles.contact_info_main} style={{padding:'1em'}}>
                    <div>
                        <Typography className={styles.contact_info_name}>
                            <span>
                                {_.get(this.props, "participant.first_name")}{'\t'}
                                {_.get(this.props, "participant.last_name")}
                            </span>
                        </Typography>
                        <StyledContact className={styles.contact_info_phone}>
                            <span>
                                {phone}
                            </span>
                        </StyledContact>
                        <Typography className={styles.contact_info_email}>
                            <span>
                                {_.get(this.props, "participant.email")}
                            </span>
                        </Typography>
                        <Typography className={styles.contact_info_address}>
                            <span style={{"textTransform":"uppercase"}}>
                                {_.get(this.props, "participant.mailing_street")}{'\t'}
                                {_.get(this.props, "participant.mailing_city")}{'\t'}
                            </span>
                        </Typography>
                    </div>
                </Paper>
            </Container>
        );
    }
}


export default ContactInfo;