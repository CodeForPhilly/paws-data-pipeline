import React, { Component } from 'react';
import { Paper, Typography, Container} from '@material-ui/core';
import { withStyles } from '@material-ui/core/styles';

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

        return (<Container>
            <Typography align='center' gutterBottom='true' variant='h4'>Contact Info</Typography>
                <Paper variant='outlined' style={{padding:'1em'}}>
                    <div style={{"display":"flex", "justifyContent":"space-between"}}>
                        <Typography>
                            <span style={{'fontWeight':'600'}}>
                                {'Name:\t'}
                            </span>
                            <span>
                                {_.get(this.props, "participant.first_name")}{'\t'}
                                {_.get(this.props, "participant.last_name")}
                            </span>
                        </Typography>
                        <StyledContact>
                            <span style={{'fontWeight':'600'}}>
                                {'Phone:\t'}
                            </span>
                            <span>
                                {phone}
                            </span>
                        </StyledContact>
                        <Typography>
                        <span style={{'fontWeight':'600'}}>
                                {'Email:\t'}
                            </span>
                            <span>
                                {_.get(this.props, "participant.email")}
                            </span>
                        </Typography>
                    </div>
                <Typography>
                    <span style={{'fontWeight':'600'}}>
                        {'Address:\t'}
                    </span>
                    <span style={{"textTransform":"uppercase"}}>
                        {_.get(this.props, "participant.mailing_street")}{'\t'}
                        {_.get(this.props, "participant.mailing_city")}{'\t'}
                    </span>
                </Typography>
            </Paper>
        </Container>
        );
    }
}


export default ContactInfo;