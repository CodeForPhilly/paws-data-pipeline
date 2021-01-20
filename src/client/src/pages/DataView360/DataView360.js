import React, {Component} from 'react';
import {withStyles} from '@material-ui/core/styles';
import {
    Paper,
    Container,
    Box,
    Table,
    TableBody,
    TableCell,
    TableContainer,
    TableHead,
    TableRow
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
        minWidth: 700,
    },
    headerCell: {
        fontWeight: "bold"
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
            participantData: undefined,
            isDataBusy: false,
            participantList: [],
            participantTable: undefined
        }

        //this.handleGetParticipant = this.handleGetParticipant.bind(this);
        this.handleSearchChange = this.handleSearchChange.bind(this);
    }

    /*
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
    */

    renderParticipantsTable() {
        const {classes} = this.props;
        const tableRowColors = ["#a3ddcb", "#e8e9a1", "#e6b566", "#e5707e", "#00af91"]

        let participantListGrouped = _.groupBy(this.state.participantList, "matching_id");
        participantListGrouped = _.reverse(_.sortBy(participantListGrouped, matching_group => {
            return _.size(matching_group);
        }));

        return (
            <Paper className={classes.tableCard}>
                <TableContainer className={classes.container}>
                    <Table className={classes.table} stickyHeader aria-label="sticky table">
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
                                            <TableCell align="left">{row.matching_id}</TableCell>
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
            </Paper>)
    }

    async handleSearchChange(search_participant) {
        this.setState({isDataBusy: true});

        await new Promise(resolve => setTimeout(resolve, 1000));
        let response = await fetch(`/api/contacts/${search_participant}`);
        response = await response.json();

        await this.setState({participantList: response.result})

        this.state.participantTable = this.renderParticipantsTable();
        this.setState({isDataBusy: false});
    }

    render() {
        const {classes} = this.props;
        return (
            <Container>
                <SearchBar participant={this.state.participant}
                           handleParticipantChange={this.handleGetParticipant}
                           handleSearchChange={this.handleSearchChange}/>
                {(_.isEmpty(this.state.participantTable) !== true && this.state.isDataBusy !== true) && (
                    <Container className={styles.main} elevation={1} style={{"padding": "1em"}}>
                        {this.state.participantTable}
                    </Container>
                )}
                {(_.isEmpty(this.state.participantData) !== true && this.state.isDataBusy !== true) && (
                    <Paper className={styles.main} elevation={1} style={{"padding": "1em"}}>
                        <ContactInfo participant={_.get(this.state, "participantData.salesforcecontacts")}/>
                        <Donations donations={_.get(this.state, 'participantData.salesforcedonations')}/>
                        <Adoptions adoptions={_.get(this.state, 'participantData.shelterluvpeople')}/>
                        <Volunteer volunteer={_.get(this.state, 'participantData.volgistics.json')}
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