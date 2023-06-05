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
    const [fileListHtml, setFileListHtml] = React.useState(undefined);
    const [lastExecution, setLastExecution] = React.useState(undefined);
    const [isNewFileExist, setIsNewFileExist] = React.useState(false);


    React.useEffect(() => {
        (async () => {
            await refreshPage();
        })()
    }, [])

    const refreshPage = async () => {
        setIsLoading(true);

        const filesData = await fetch("/api/listCurrentFiles",
            {
                method: 'GET',
                headers: {
                    'Authorization': 'Bearer ' + props.access_token
                }
            });
        const filesResponse = await filesData.json();

        setFileListHtml(filesResponse);

        const statsData = await fetch("/api/statistics",
            {
                method: 'GET',
                headers: {
                    'Authorization': 'Bearer ' + props.access_token
                }
            });
        const statsResponse = await statsData.json()

        handleGetStatistics(statsResponse);
        determineNewFileExist(statsResponse, filesResponse);

        setIsLoading(false);
    }

    // sets newFileExists to true if one of the files was uploaded after last execution
    const determineNewFileExist = (statsResponse, filesResponse) => {
        let lastExecutionTime = statsResponse.executionTime;

        let filesUploadedAfterExecution =_.filter(filesResponse, fileName => {
            let fileTimestampAndType = fileName.substring(fileName.indexOf('-') + 1)
            let fileTimestamp = fileTimestampAndType.split('.')[0]
            let fileTimestampMoment = moment(fileTimestamp, "YYYY-MM-DD--HH-mm-ss");

            let result = moment(fileTimestampMoment).isAfter(lastExecutionTime);

            return result;
        });

        if (_.isEmpty(filesUploadedAfterExecution) === false) {
            setIsNewFileExist(true);
        }
        else {
            setIsNewFileExist(false);
        }
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
                            <Grid item>
                                <Paper style={{padding: 5, marginTop: 10}}>
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

                        </Grid>
                    </Grid>
                </Paper>
            }

        </Container>
    );
}