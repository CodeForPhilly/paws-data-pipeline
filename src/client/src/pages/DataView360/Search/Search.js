import React, {Component} from 'react';
import {withStyles} from '@material-ui/core/styles';
import {withRouter} from "react-router";
import {matchPath} from "react-router";

import {
    Paper,
    Container,
    Table,
    TableBody,
    TableCell,
    TableContainer,
    TableHead,
    TableRow,
    Typography,
    Box,
    Backdrop,
    CircularProgress
} from '@material-ui/core';

import _ from 'lodash';
import SearchBar from './components/SearchBar';
import {formatPhoneNumber} from "../../../utils/utils";
import Grid from "@material-ui/core/Grid";


const customStyles = theme => ({
    backdrop: {
        zIndex: theme.zIndex.drawer + 1,
        color: '#fff',
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

class Search360 extends Component {

    constructor(props) {
        super(props);

        this.state = {
            search_participant: '',
            isDataBusy: false,
            participantList: [],
            participantTable: undefined
        }

        this.onRowClick = this.onRowClick.bind(this);
        this.handleSearchChange = this.handleSearchChange.bind(this);
    }

    async componentDidMount() {
        let state = _.get(this.props, 'location.state');
        if (_.isEmpty(state) !== true) {
            let stateData = JSON.parse(state);
            await this.setState({
                search_participant: stateData.participant,
                participantList: stateData.participantList
            })

            this.state.participantTable = this.renderParticipantsTable();

        }
    }

    onRowClick(matching_id) {
        const match = matchPath(`/360view/view/${matching_id}`, {
            path: "/360view/view/:matching_id",
            exact: true,
            params: {matching_id}
        });
        this.props.history.push(match.url,
            {

                state: JSON.stringify((
                    {
                        participant: this.state.search_participant,
                        participantList: this.state.participantList
                    }
                ))
            })
    }

    renderParticipantsTable() {
        const {classes} = this.props;
        const tableRowColors = [classes.tableRowEven, classes.tableRowOdd]

        let participantListGrouped = _.groupBy(this.state.participantList, "matching_id");
        participantListGrouped = _.reverse(_.sortBy(participantListGrouped, matching_group => {
            return _.size(matching_group);
        }));

        return (
            <Grid container direction={"column"} justify={"center"}>
                <Grid container direction={"row"} justify={"center"}>
                    <Grid item>
                        <Box pt={2} pb={4}>
                            <Typography>You searched for <b>{this.state.search_participant}</b></Typography>
                        </Box>

                    </Grid>
                </Grid>
                <Grid container direction={"row"} justify={"center"}>

                    <Paper>
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
                                                                 onClick={() => this.onRowClick(row.matching_id)}>
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
                </Grid>
            </Grid>
        )
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
        });
    }

    render() {
        const {classes} = this.props;

        return (
            <Container>
                <SearchBar participant={this.state.participant}
                           handleParticipantChange={this.onRowClick}
                           handleSearchChange={this.handleSearchChange}/>

                {this.state.isDataBusy === true ?
                    <Backdrop className={classes.backdrop} open={this.state.isLoading !== false}>
                        <CircularProgress size={60}/>
                    </Backdrop> :
                    _.isEmpty(this.state.participantTable) !== true &&
                    <Container>
                        {this.state.participantTable}
                    </Container>
                }
            </Container>
        );
    }
}

export default withRouter(withStyles(customStyles)(Search360));