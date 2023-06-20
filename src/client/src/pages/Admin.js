import React from 'react';
import {
    Grid,
    Paper,
    Button,
    TableHead,
    Backdrop,
    CircularProgress,
    CardContent,
    TableRow,
    TableContainer,
    TableCell,
    TableBody,
    Table, Container, Typography
} from "@material-ui/core";

import _ from 'lodash';
import moment from "moment";
import {Alert} from "@material-ui/lab";
import Box from "@material-ui/core/Box";
import {makeStyles} from "@material-ui/styles";

const useStyles = makeStyles({});

export default function Admin(props) {
    const [isLoading, setIsLoading] = React.useState(undefined);
    const [statistics, setStatistics] = React.useState(undefined);
    const [filesInput, setFilesInput] = React.useState(undefined);
    const [lastExecution, setLastExecution] = React.useState(undefined);


    React.useEffect(() => {
        (async () => {
            await refreshPage();
        })()
    }, [])

    const refreshPage = async () => {
        setIsLoading(true);

        const statsData = await fetch("/api/statistics",
            {
                method: 'GET',
                headers: {
                    'Authorization': 'Bearer ' + props.access_token
                }
            });
        const statsResponse = await statsData.json()

        handleGetStatistics(statsResponse);

        setIsLoading(false);
    }

    const handleUpload = async (event) => {
        event.preventDefault();

        setIsLoading(true);

        let formData = new FormData();

        let files = _.get(event, 'target.[0].files');
        _.forEach(files, element => {
            formData.append('file', element, element.name)
        })

        await fetch("/api/file", {
            method: 'POST',
            body: formData,
            headers: {
                'Authorization': 'Bearer ' + props.access_token
            }
        })

        setIsLoading(false);
        setFilesInput(undefined);

        await refreshPage();
    };

    const handleExecute = async (event) => {
        event.preventDefault();

        setIsLoading(true);

        await fetch('/api/execute',
            {
                method: 'POST',
                headers: {
                    'Authorization': 'Bearer ' + props.access_token
                }
            });

        await refreshPage();
    }

    const handleGetStatistics = (statsResponse) => {
        if (statsResponse !== 'executing') {
            setStatistics(_.toPairsIn(statsResponse.stats));
            setLastExecution(statsResponse.executionTime)

        } else {
            setStatistics(statsResponse);
        }
    }

    return (
        <Container>
            <Box display="flex" justifyContent="center" pb={3}>
                <Typography variant={"h2"}>Admin Portal</Typography>
            </Box>
            {isLoading === true ?
                <Backdrop open={true}>
                    <CircularProgress size={60}/>
                </Backdrop> :
                <Paper elevation={1} style={{"padding": "2em"}}>
                    {statistics === 'Running' && <Alert severity="info">Execution is in Progress...</Alert>}

                    <Grid container item spacing={5} direction="row" style={{padding: 20}}>
                        <Grid container item direction="column" spacing={3} sm={6}>
                            {_.isEmpty(fileListHtml) !== true &&
                                <>
                                    <Grid item>
                                        <Typography variant="h5">Latest Files</Typography>
                                    </Grid>
                                    <Grid item>
                                            <TableContainer component={Paper}>
                                                <Table aria-label="simple table">
                                                    <TableHead>
                                                        <TableRow>
                                                            <TableCell><b>File Type</b></TableCell>
                                                            <TableCell><b>Last Updated</b></TableCell>
                                                        </TableRow>
                                                    </TableHead>
                                                    <TableBody>
                                                        {_.map(fileListHtml, (file, index) => {
                                                            const fileName = file.split("-")[0];
                                                            let fileDate = file.split("-").slice(1).join().split(".")[0];
                                                            let fileDateOnlyNumbers = fileDate.replaceAll(",", "");
                                                            let fileDateFormatted = moment(fileDateOnlyNumbers, "YYYYMMDDhmmss").local().format("MMMM Do YYYY, h:mm:ss a");

                                                            return (
                                                                <TableRow key={index}>
                                                                    <TableCell>{fileName}</TableCell>
                                                                    <TableCell>{fileDateFormatted}</TableCell>
                                                                </TableRow>
                                                            )
                                                        })
                                                        }
                                                    </TableBody>
                                                </Table>
                                            </TableContainer>
                                    </Grid>
                                </>
                            }
                            <Grid item>
                                <Paper>
                                    <CardContent>
                                        <Typography variant="h5">Upload Files</Typography>
                                        <Typography variant="caption">Note: This upload feature now only accepts Volgistics data files. Other data is uploaded automatically.</Typography>
                                        <form onSubmit={handleUpload}>
                                            <input type="file" id="fileItemsID"
                                                   value={filesInput}
                                                   multiple
                                            />
                                            <Button type="submit" variant="contained" color="primary"
                                                    disabled={statistics === 'Running'}>
                                                Upload
                                            </Button>
                                        </form>
                                    </CardContent>
                                </Paper>
                            </Grid>
                        </Grid>
                        <Grid container item direction="column" spacing={3} sm={6}>
                            <Grid item>
                                <Paper style={{ padding: 5 }}>
                                    <CardContent>
                                        <Typography variant="h5" styles={{paddingBottom: 5}}>Run New Analysis</Typography>
                                        <form onSubmit={handleExecute}>
                                            <Button type="submit" variant="contained" color="primary"
                                                    disabled={statistics === 'Running'}>
                                                Run Data Analysis
                                            </Button>
                                        </form>
                                    </CardContent>
                                </Paper>
                            </Grid>
                            <Grid item>
                                <Typography variant="h5">Last Match Analysis</Typography>
                            </Grid>
                            <Grid item>
                                {_.isEmpty(statistics) !== true &&
                                    statistics !== 'Running' &&
                                    <TableContainer component={Paper}>
                                        <Table aria-label="simple table">
                                            <TableBody>
                                                <TableRow key='time'>
                                                    <TableCell align="left" component="th" scope="row">
                                                        <b>Last Analysis</b>
                                                    </TableCell>
                                                    <TableCell align="left">
                                                        <b>
                                                            {moment(lastExecution, "dddd MMMM Do h:mm:ss YYYY").local().format("MMMM Do YYYY, h:mm:ss a")}
                                                        </b>
                                                    </TableCell>
                                                </TableRow>
                                                {statistics.map((row, index) => (
                                                    <TableRow key={index}>
                                                        <TableCell align="left" component="th" scope="row">
                                                            {row[0]}
                                                        </TableCell>
                                                        <TableCell align="left">{row[1]}</TableCell>
                                                    </TableRow>
                                                ))}
                                            </TableBody>
                                        </Table>
                                    </TableContainer>
                                }
                            </Grid>

                        </Grid>
                    </Grid>
                </Paper>
            }

        </Container>
    );
}