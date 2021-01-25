import React, {Component} from 'react';
import {withStyles} from '@material-ui/core/styles';
import {
    Paper,
    Container,
    Box,
    Button,
    Link,
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

import SearchBar from './components/SearchBar';
import ContactInfo from './components/ContactInfo';
import Volunteer from './components/Volunteer';
import Donations from './components/Donations';
import Adoptions from './components/Adoptions';


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

    renderParticipantsTable() {
        const {classes} = this.props;
        const tableRowColors = ["#FFFFFF", "#E8E8E8"]

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
                                        return _.map(row_group, row => {
                                            return <TableRow key={row.source_id}
                                                            style={{backgroundColor: tableRowColors[index % _.size(tableRowColors)]}}>
                                                <TableCell align="left"><Link href="#" onClick={() => this.handleGetParticipant(row.matching_id)}>{row.matching_id}</Link></TableCell>
                                                <TableCell align="left">{row.first_name}</TableCell>
                                                <TableCell align="left">{row.last_name}</TableCell>
                                                <TableCell align="left">{row.email}</TableCell>
                                                <TableCell align="left">{row.mobile}</TableCell>
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
                        <Button variant="contained" color="primary" className={styles.back_button} 
                            onClick={() => { 
                                this.setState({showParticipant: false, showTable: true, showSearchBar: true }) 
                            }}>Back to Results</Button>
                        <Donations donations={_.get(this.state, 'participantData.donations')}/>
                        <Adoptions adoptions={_.get(this.state, 'participantData.adoptions')}/>
                        <Volunteer volunteer={_.get(this.state, 'participantData.shifts')}
                                   volunteerShifts={_.get(this.state, 'participantData.volgistics_shifts_results')}/>

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