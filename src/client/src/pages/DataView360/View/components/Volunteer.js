import React, { Component } from 'react';
import _ from 'lodash';
import VolunteerActivity from './VolunteerActivity';
import VolunteerHistory from './VolunteerHistory';


class Volunteer extends Component {

    render() {
        return (
            <React.Fragment>
                <VolunteerActivity volunteer={this.props.volunteer} />
                <VolunteerHistory volunteerShifts={this.props.volunteerShifts} />
            </React.Fragment>
        );
    }
}

export default Volunteer;