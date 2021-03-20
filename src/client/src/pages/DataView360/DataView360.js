import React, {Component} from 'react';
import {withStyles} from '@material-ui/core/styles';
import {
    Paper,
    Container,
    Box,
    Button,
    Grid,
    Table,
    TableBody,
    TableCell,
    TableContainer,
    TableHead,
    TableRow,
    Typography
} from '@material-ui/core';
import CircularProgress from '@material-ui/core/CircularProgress';
import styles from "./styles/DataView360.module.css";
import _ from 'lodash';
import moment from 'moment';
import SearchBar from './components/SearchBar';
import ContactInfo from './components/ContactInfo';
import Volunteer from './components/Volunteer';
import Donations from './components/Donations';
import Adoptions from './components/Adoptions';
import {formatPhoneNumber} from "../../utils/utils";


const customStyles = theme => ({
    spinner: {
        display: 'flex',
        align: 'center'
    },
    tableCard: {
        width: '100%',
    },
    table: {
        minWidth: 700
    },
    tableRowEven: {
        backgroundColor: "#FFFFFF",
        "&:hover": {
            backgroundColor: "#E6F7FF",
            cursor: "pointer"
        }
    },
    tableRowOdd: {
        backgroundColor: "#E8E8E8",
        "&:hover": {
            backgroundColor: "#CCEEFF",
            cursor: "pointer"
        }
    },
    headerCell: {
        fontWeight: "bold",
        minWidth: 60,
        backgroundColor: "#A9A9A9"
    },
    container: {
        maxHeight: 600,
    },
});

class DataView360 extends Component {
    constructor(props) {
        super(props);

        this.state = {
            search_participant: '',
            participantData: {},
            isDataBusy: false,
            participantList: [],
            participantTable: undefined,
            showParticipant: false,
            showTable: true,
            showSearchBar: true
        }

        this.extractVolunteerActivity = this.extractVolunteerActivity.bind(this);
        this.handleGetParticipant = this.handleGetParticipant.bind(this);
        this.handleSearchChange = this.handleSearchChange.bind(this);
    }

    async handleGetParticipant(matching_id) {
        this.setState({isDataBusy: true, showSearchBar: false});

        await new Promise(resolve => setTimeout(resolve, 1000));
        let response = await fetch(`/api/360/${matching_id}`);
        response = await response.json();

        this.setState({
            participantData: response.result,
            isDataBusy: false,
            showParticipant: true,
            showTable: false,
            showSearchBar: false
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

    renderParticipantsTable() {
        const {classes} = this.props;
        const tableRowColors = [classes.tableRowEven, classes.tableRowOdd]

        let participantListGrouped = _.groupBy(this.state.participantList, "matching_id");
        participantListGrouped = _.reverse(_.sortBy(participantListGrouped, matching_group => {
            return _.size(matching_group);
        }));

        return (
            <Container>
                <Typography paragraph={true}>You searched for <b>{this.state.search_participant}</b></Typography>
                <Paper className={classes.tableCard}>
                    <TableContainer className={classes.container}>
                        <Table className={classes.table} size="small" stickyHeader aria-label="sticky table">
                            <TableHead>
                                <TableRow>
                                    <TableCell align="left" className={classes.headerCell}>Match ID</TableCell>
                                    <TableCell align="left" className={classes.headerCell}>First Name</TableCell>
                                    <TableCell align="left" className={classes.headerCell}>Last Name</TableCell>
                                    <TableCell align="left" className={classes.headerCell}>Email</TableCell>
                                    <TableCell align="left" className={classes.headerCell}>Mobile</TableCell>
                                    <TableCell align="left" className={classes.headerCell}>Source</TableCell>
                                    <TableCell align="left" className={classes.headerCell}>ID in Source</TableCell>
                                </TableRow>
                            </TableHead>
                            <TableBody>
                                {
                                    _.map(participantListGrouped, (row_group, index) => {
                                        return _.map(row_group, (row, idx) => {
                                            return <TableRow key={`${row.source_id}${idx}`}
                                                             className={tableRowColors[index % _.size(tableRowColors)]}
                                                             onClick={() => this.handleGetParticipant(row.matching_id)}>
                                                <TableCell align="left">{row.matching_id}</TableCell>
                                                <TableCell align="left">{row.first_name}</TableCell>
                                                <TableCell align="left">{row.last_name}</TableCell>
                                                <TableCell align="left">{row.email}</TableCell>
                                                <TableCell align="left">{formatPhoneNumber(row.mobile)}</TableCell>
                                                <TableCell align="left">{row.source_type}</TableCell>
                                                <TableCell align="left">{row.source_id}</TableCell>
                                            </TableRow>
                                        })
                                    })
                                }
                            </TableBody>
                        </Table>
                    </TableContainer>
                </Paper>
            </Container>)
    }

    async handleSearchChange(search_participant) {
        this.setState({isDataBusy: true, search_participant: search_participant});

        await new Promise(resolve => setTimeout(resolve, 1000));
        let response = await fetch(`/api/contacts/${search_participant}`);
        response = await response.json();

        await this.setState({participantList: response.result})

        this.state.participantTable = this.renderParticipantsTable();
        this.setState({
            isDataBusy: false,
            showParticipant: false,
            showTable: true
        });
    }

    render() {
        const {classes} = this.props;
        return (
            <Container>
                {this.state.showSearchBar &&
                (<SearchBar participant={this.state.participant}
                            handleParticipantChange={this.handleGetParticipant}
                            handleSearchChange={this.handleSearchChange}/>
                )}
                {(_.isEmpty(this.state.participantTable) !== true &&
                    this.state.isDataBusy !== true &&
                    this.state.showTable === true &&
                    this.state.showParticipant === false) && (
                    <Container className={styles.main} elevation={1} style={{"padding": "1em"}}>
                        {this.state.participantTable}
                    </Container>
                )}
                {(_.isEmpty(this.state.participantData) !== true &&
                    this.state.isDataBusy !== true &&
                    this.state.showParticipant === true) && (
                    <Paper className={styles.main} elevation={1} style={{"padding": "1em"}}>
                        <ContactInfo participant={_.get(this.state, 'participantData.contact_details')}/>
                        <Grid container direction="row" justify="center">
                            <Grid item style={{"marginTop": "1em", "position": "fixed"}}>
                                <Button variant="contained" color="primary"
                                        onClick={() => {
                                            this.setState({
                                                showParticipant: false,
                                                showTable: true,
                                                showSearchBar: true
                                            })
                                        }}>Back to Results
                                </Button>
                            </Grid>
                        </Grid>
                        <Donations donations={_.get(this.state, 'participantData.donations')}/>
                        <Adoptions adoptions={_.get(this.state, 'participantData.adoptions')}/>
                        <Volunteer volunteer={this.extractVolunteerActivity()}
                                   volunteerShifts={_.get(this.state, 'participantData.shifts')}/>

                    </Paper>)}
                {this.state.isDataBusy === true && (
                    <Box display="flex" justifyContent="center" className={classes.spinner}>
                        <CircularProgress/>
                    </Box>
                )}
            </Container>
        );
    }
}

export default withStyles(customStyles)(DataView360);