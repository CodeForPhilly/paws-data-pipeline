import React from 'react';
import {matchPath} from "react-router";
import {useHistory} from "react-router-dom";
import {makeStyles} from '@material-ui/styles';

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

import _, {lowerCase} from 'lodash';
import SearchBar from './components/SearchBar';
import {formatPhoneNumber} from "../../../utils/utils";
import Grid from "@material-ui/core/Grid";

const useStyles = makeStyles({
    table: {
        "&:hover": {
            backgroundColor: "#E6F7FF",
            cursor: "pointer"
        }
    },
    tableRowEven: {
        backgroundColor: "#FFFFFF"
    },
    tableRowOdd: {
        backgroundColor: "#E8E8E8"
    },
    container: {
        maxHeight: 600,
    },
    narrowCell: {
        'width': '150px',
    }
});

export const Search360 = (props) => {
    const history = useHistory();
    const classes = useStyles();

    const [searchParticipant, setSearchParticipant] = React.useState('');
    const [isLoading, setIsLoading] = React.useState(false);
    const [participantList, setParticipantList] = React.useState(undefined);


    React.useEffect(() => {
        (async () => {
            let state = _.get(history, 'location.state');
            if (_.isEmpty(state) !== true) {
                let stateData = JSON.parse(state);
                await setSearchParticipant(stateData.participant);
                await setParticipantList(stateData.participantList)
            }
        })();
    }, []);

    const onRowClick = (matching_id) => {
        const match = matchPath(`/360view/view/${matching_id}`, {
            path: "/360view/view/:matching_id",
            exact: true,
            params: {matching_id}
        });
        history.push(match.url, {
            state: JSON.stringify((
                {
                    participant: searchParticipant,
                    participantList: participantList,
                    url: `/360view/search`
                }
            ))
        })
    }

    const namesToLowerCase = (participant) => {
        let first_name = participant.first_name
        let last_name = participant.last_name

        return {
            ...participant,
            lower_first_name: lowerCase(first_name),
            lower_last_name: lowerCase(last_name)
        }
    }

    const renderParticipantsTable = () => {
        const tableRowColors = [classes.tableRowEven, classes.tableRowOdd]

        let participantListGrouped = _.map(participantList, namesToLowerCase)
        participantListGrouped = _.groupBy(participantListGrouped, "matching_id");
        participantListGrouped = _.orderBy(participantListGrouped, ['0.lower_last_name', '0.lower_first_name']);

        return (
            <Grid container direction={"column"}>
                <Grid container direction={"row"} justify={"center"}>
                    <Grid item>
                        <Box pt={2} pb={4}>
                            <Typography>You searched for <b>{searchParticipant}</b></Typography>
                        </Box>

                    </Grid>
                </Grid>
                <Grid container direction={"row"}>
                    <Paper>
                        <TableContainer className={classes.container}>
                            <Table className={classes.table} size="small" stickyHeader aria-label="sticky table">
                                <TableHead>
                                    <TableRow>
                                        <TableCell width="5%">Match ID</TableCell>
                                        <TableCell width="5%">First Name</TableCell>
                                        <TableCell width="5%">Last Name</TableCell>
                                        <TableCell width="5%">Email</TableCell>
                                        <TableCell width="10%">Mobile</TableCell>
                                        <TableCell width="10%">RFM Score</TableCell>
                                        <TableCell width="10%">Source</TableCell>
                                        <TableCell width="10%">ID in Source</TableCell>
                                    </TableRow>
                                </TableHead>
                                <TableBody>
                                    {
                                        _.map(participantListGrouped, (row_group, index) => {
                                            return _.map(row_group, (row, idx) => {
                                                return <TableRow key={`${row.source_id}${idx}`}
                                                                 className={[classes.table, tableRowColors[index % _.size(tableRowColors)]].join(" ")}
                                                                 onClick={() => onRowClick(row.matching_id)}>
                                                    <TableCell>{row.matching_id}</TableCell>
                                                    <TableCell>{row.first_name}</TableCell>
                                                    <TableCell>{row.last_name}</TableCell>
                                                    <TableCell>{row.email}</TableCell>
                                                    <TableCell>{formatPhoneNumber(row.mobile)}</TableCell>
                                                    <TableCell
                                                               style={{
                                                                   backgroundColor: row.rfm_color,
                                                                   color: row.rfm_text_color
                                                               }}>
                                                        {row.rfm_score} ({row.rfm_label})
                                                    </TableCell>
                                                    <TableCell>{row.source_type}</TableCell>
                                                    <TableCell>{row.source_id}</TableCell>
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

    const handleSearchChange = async (search_participant) => {
        setIsLoading(true);
        setSearchParticipant(search_participant);

        let response = await fetch(`/api/contacts/${search_participant}`,
            {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer ' + props.access_token
                }
            }
        );
        response = await response.json();

        await setParticipantList(response.result);

        setIsLoading(false);
    }

    return (
        <Container maxWidth={"lg"}>
            <Box display="flex" justifyContent="center" pb={3}>
                <Typography variant={"h2"}>PAWS Contact Search</Typography>
            </Box>
            <SearchBar participant={searchParticipant}
                       handleParticipantChange={onRowClick}
                       handleSearchChange={handleSearchChange}/>

            {isLoading === true ?
                <Backdrop open={isLoading !== false}>
                    <CircularProgress size={60}/>
                </Backdrop> :
                (participantList && _.isEmpty(participantList) !== true) ?
                    renderParticipantsTable()
                    : participantList && _.isEmpty(participantList) === true &&
                    <Box display="flex" justifyContent="center" pt={5}>
                        <Typography variant={"h5"}>No Results</Typography>
                    </Box>
            }
        </Container>
    );
}
