import React from 'react';
import {matchPath} from "react-router";

import {
    Backdrop,
    Button,
    CircularProgress,
    Container,
    Paper,
    Table,
    TableBody,
    TableCell,
    TableContainer,
    TableHead,
    TableRow
} from '@material-ui/core';
import _ from 'lodash';
import Typography from "@material-ui/core/Typography";
import Grid from "@material-ui/core/Grid";
import Box from "@material-ui/core/Box";
import {makeStyles} from "@material-ui/styles";
import {formatPhoneNumber} from "../../utils/utils";
import {useHistory} from "react-router-dom";

const RFM_LIMIT = 100

const useStyles = makeStyles({
    container: {
        maxHeight: 600,
    },
    tableRow: {
        "&:hover": {
            backgroundColor: "#E6F7FF",
            cursor: "pointer"
        }
    },
});

export function RFM(props) {
    const classes = useStyles();
    const history = useHistory();

    const [labels, setLabels] = React.useState([]);
    const [selectedLabel, setSelectedLabel] = React.useState("");
    const [participants, setParticipants] = React.useState(undefined);
    const [isLoading, setIsLoading] = React.useState(false);

    React.useEffect(() => {
        setIsLoading(true);

        (async () => {
            let labelsResponse = await fetch(`/api/rfm/labels`,
                {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': 'Bearer ' + props.access_token
                    }
                });
            labelsResponse = await labelsResponse.json();
            setLabels(labelsResponse.result);

            try {
                let state = JSON.parse(_.get(history, 'location.state'));
                let stateLabel = state.selectedLabel;
                if (stateLabel) {
                    await handleLabelChange(stateLabel);
                }
            } catch {
            }

            setIsLoading(false);

        })();
    }, []);

    const handleLabelChange = async (labelData) => {
        setIsLoading(true);

        try {
            setSelectedLabel(labelData);
            let participantsResponse = await fetch(`/api/rfm/${labelData.rfm_label}/${RFM_LIMIT}`,
                {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': 'Bearer ' + props.access_token
                    }
                });
            participantsResponse = await participantsResponse.json();

            setParticipants(_.uniqBy(participantsResponse.result, 'matching_id'));
        } finally {
            setIsLoading(false);
        }

    };

    const onRowClick = (matching_id) => {
        const match = matchPath(`/360view/view/${matching_id}`, {
            path: "/360view/view/:matching_id",
            exact: true,
            params: {matching_id}
        });
        history.push(match.url, {
            state: JSON.stringify((
                {
                    url: `/rfm`,
                    selectedLabel
                }
            ))
        })
    }

    return (
        <Container maxWidth={"xl"}>
            <Box display="flex" justifyContent="center" pb={5}>
                <Typography variant={"h2"}>RFM Scores</Typography>
            </Box>
            {isLoading === true ?
                <Backdrop open={isLoading !== false}>
                    <CircularProgress size={60}/>
                </Backdrop> :

                <Grid container item direction="row">
                    <Grid container item direction="column" sm={3}>
                        <Grid item>

                            {_.isEmpty(labels) !== true &&
                            <Grid item container direction="column" spacing={3}>
                                <Grid item>
                                    <Typography variant={"h5"}>
                                        RFM Labels
                                    </Typography>
                                </Grid>
                                <Grid container item direction="column" spacing={2}>
                                    {
                                        labels.map((labelData, index) => {
                                            return <Grid item key={index}>
                                                <Button onClick={() => handleLabelChange(labelData)}
                                                        style={{
                                                            backgroundColor: labelData.rfm_color,
                                                            minWidth: 300,
                                                            border: labelData === selectedLabel ? "solid" : "none",
                                                        }}>
                                                    <Typography style={{
                                                        color: labelData.rfm_text_color,
                                                        padding: 3
                                                    }}>
                                                        {labelData.rfm_label} ({labelData.count})
                                                    </Typography>
                                                </Button>
                                            </Grid>
                                        })
                                    }
                                </Grid>
                            </Grid>}

                        </Grid>
                    </Grid>
                    <Grid container item direction="column" sm={8}>
                        <Grid item>
                            {participants &&
                            <Grid container direction="column" spacing={10}>
                                <Grid item>
                                    <Typography variant={"h5"}>
                                        Showing {RFM_LIMIT} Results:
                                    </Typography>
                                </Grid>
                                <Grid item>
                                    <Paper>
                                        <TableContainer className={classes.container}>
                                            <Table size="small" stickyHeader aria-label="sticky table">
                                                <TableHead>
                                                    <TableRow>
                                                        <TableCell align="left">First Name</TableCell>
                                                        <TableCell align="left">Last Name</TableCell>
                                                        <TableCell align="left">Email</TableCell>
                                                        <TableCell align="left">Mobile</TableCell>
                                                        <TableCell align="left">RFM</TableCell>
                                                        <TableCell align="left">Salesforce ID</TableCell>
                                                    </TableRow>
                                                </TableHead>
                                                <TableBody>
                                                    {
                                                        _.map(participants, (row, index) => {
                                                            return <TableRow key={`${row.source_id}${index}`}
                                                                             onClick={() => onRowClick(row.matching_id)}
                                                                             className={classes.tableRow}>
                                                                <TableCell align="left">{row.first_name}</TableCell>
                                                                <TableCell align="left">{row.last_name}</TableCell>
                                                                <TableCell align="left">{row.email}</TableCell>
                                                                <TableCell
                                                                    align="left">{formatPhoneNumber(row.mobile)}</TableCell>
                                                                <TableCell
                                                                    align="left">{row.rfm_score} ({row.rfm_label})</TableCell>
                                                                <TableCell align="left">{row.source_id}</TableCell>
                                                            </TableRow>
                                                        })
                                                    }
                                                </TableBody>
                                            </Table>
                                        </TableContainer>
                                    </Paper>
                                </Grid>
                            </Grid>
                            }
                        </Grid>
                    </Grid>

                </Grid>

            }

        </Container>
    );

}