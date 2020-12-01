import React, {Component} from 'react';
import { withStyles } from '@material-ui/core/styles';
import { Paper, Container} from '@material-ui/core';
import CircularProgress from '@material-ui/core/CircularProgress';
import Box from '@material-ui/core/Box';
import styles from "./styles/DataView360.module.css";
import _ from 'lodash';

import SearchBar from './components/SearchBar';
import ContactInfo from './components/ContactInfo';
import Volunteer from './components/Volunteer';
import Donations from './components/Donations';
import Adoptions from './components/Adoptions';


const customStyles = theme => ({
    spinner: {
        display: 'flex',
        align: 'center',
        marginLeft: theme.spacing(2)
    }
});


class DataView360 extends Component {
    constructor(props) {
        super(props);

        this.state = {
            participant: 'DEFAULT',
            participantData: undefined,
            isDataBusy: false
        }

        this.handleGetParticipant = this.handleGetParticipant.bind(this);
        this.handleSearchChange = this.handleSearchChange.bind(this);
    }

    async handleGetParticipant(event) {
        const participant = _.get(event, "target.value");
        this.setState({participant: participant});
        this.setState({isDataBusy: true});

        await new Promise(resolve => setTimeout(resolve, 1000));
        let response = await fetch(`/api/360/${participant}`);
        response = await response.json();

        this.setState({participantData: response});
        this.setState({isDataBusy: false});
    }

    handleSearchChange() {
        this.setState({participantData: undefined});
        this.setState({participant: 'DEFAULT'});
    }

    render(){
        const { classes } = this.props;

        return(
            <Container>
                <SearchBar participant={this.state.participant}
                handleParticipantChange={this.handleGetParticipant}
                handleSearchChange={this.handleSearchChange}/>
                {(_.isEmpty(this.state.participantData) !== true && this.state.isDataBusy !== true) && (
                <Paper className={styles.main} elevation={1} style={{"padding":"1em"}}>
                    <ContactInfo participant={_.get(this.state, "participantData.salesforcecontacts")} />
                    <Donations donations={_.get(this.state, 'participantData.salesforcedonations')} />
                    <Adoptions adoptions={_.get(this.state, 'participantData.shelterluvpeople')} />
                    <Volunteer volunteer={_.get(this.state, 'participantData.volgistics.json')}
                    volunteerShifts={_.get(this.state, 'participantData.volgistics_shifts_results')}/>

                </Paper>)}
                {this.state.isDataBusy === true && (
                    <Box display="flex" justifyContent="center" className={classes.spinner}>
                        <CircularProgress />
                    </Box>
                )}
            </Container>
        );
    }
}

export default withStyles(customStyles)(DataView360);