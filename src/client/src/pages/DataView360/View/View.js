import React, {Component} from 'react';
import {withStyles} from '@material-ui/core/styles';
import {withRouter} from "react-router";

import {
    Paper,
    Container,
    Button,
    Grid,
    Backdrop,
    CircularProgress, Box, Typography
} from '@material-ui/core';

import _ from 'lodash';
import moment from 'moment';
import ContactInfo from './components/ContactInfo';
import Volunteer from './components/Volunteer';
import Donations from './components/Donations';
import Adoptions from './components/Adoptions';
import {matchPath} from "react-router";


const customStyles = theme => ({
    backdrop: {
        zIndex: theme.zIndex.drawer + 1,
        color: '#fff',
    },
    stickyContainer: {
        position: 'fixed',
        paddingTop: 25,
        left: '-25em'
    }
});

class View360 extends Component {
    constructor(props) {
        super(props);

        this.state = {
            participantData: {},
            matchId: undefined,
            isDataBusy: false,
        }

        this.onBackClick = this.onBackClick.bind(this);
        this.extractVolunteerActivity = this.extractVolunteerActivity.bind(this);
    }

    async componentDidMount() {
        this.setState({
            isDataBusy: true,
            showSearchBar: false,
            matchId: _.last(this.props.location.pathname.split('/'))
        });

        await new Promise(resolve => setTimeout(resolve, 1000));
        let response = await fetch(`/api/360/${this.state.matchId}`,
            {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer ' + this.props.access_token
                }
            }  );
        response = await response.json();

        this.setState({
            participantData: response.result,
            isDataBusy: false
        });

    }

    extractVolunteerActivity() {
        const volgistics = _.find(this.state.participantData.contact_details, {"source_type": "volgistics"}) || {};
        let volunteerActivity = {"life_hours": 0, "ytd_hours": 0, "start_date": "N/A"}

        if (Object.keys(volgistics).length > 0) {
            const volgisticsJson = JSON.parse(volgistics.json);
            volunteerActivity = _.pick(volgisticsJson, Object.keys(volunteerActivity));
            if (volunteerActivity["start_date"] !== "") {
                volunteerActivity["start_date"] = moment(volunteerActivity["start_date"], "MM-DD-YYYY").format("YYYY-MM-DD");
            }
        }
        return volunteerActivity;
    }

    onBackClick() {
        const match = matchPath(`/360view/search`, {
            path: "/360view/search",
            exact: true
        });

        this.props.history.push(match.url, this.props.location.state.state);

    }

    render() {
        const {classes} = this.props;

        return (
            <Container>
                {(_.isEmpty(this.state.participantData) !== true &&
                    this.state.isDataBusy !== true && (
                        <Paper elevation={1} style={{"padding": "2em"}}>
                            <Grid container direction={"row"} justify={"center"}>
                                <Grid item>
                                    <Typography variant={"h4"}>Person 360 View</Typography>
                                </Grid>
                            </Grid>
                            <Grid container direction={"row"} spacing={3}>
                                <Grid item sm={4}>
                                    <Grid className={classes.stickyContainer} container direction={"column"}
                                          alignItems={"center"}>
                                        <Grid item>
                                            <ContactInfo
                                                participant={_.get(this.state, 'participantData.contact_details')}/>
                                        </Grid>
                                        <Grid item style={{"padding": "1em"}}>
                                            <Button elevation={2} variant="contained" color="primary"
                                                    onClick={() => {
                                                        this.onBackClick()
                                                    }}>Back to Results
                                            </Button>
                                        </Grid>
                                    </Grid>
                                </Grid>
                                <Grid item sm>
                                    <Grid container direction="column" style={{"marginTop": "1em"}}>
                                        <Donations donations={_.get(this.state, 'participantData.donations')}/>
                                        <Adoptions adoptions={_.get(this.state, 'participantData.adoptions')}
                                                   adoption_person_id={_.get(this.state, 'participantData.adoptions_person_id')}/>
                                        <Volunteer volunteer={this.extractVolunteerActivity()}
                                                   volunteerShifts={_.get(this.state, 'participantData.shifts')}/>
                                    </Grid>
                                </Grid>
                            </Grid>
                        </Paper>))}
                {this.state.isDataBusy === true && (
                    <Backdrop className={classes.backdrop} open={this.state.isLoading !== false}>
                        <CircularProgress size={60}/>
                    </Backdrop>
                )}
            </Container>
        );
    }
}

export default withRouter(withStyles(customStyles)(View360));