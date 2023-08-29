import React from 'react';
import {
    Grid,
    Paper,
    Button,
    Backdrop,
    CircularProgress,
    CardContent,
    Container,
    Typography,
} from "@material-ui/core";

import _ from 'lodash';
import moment from "moment-timezone";
import {Alert} from "@material-ui/lab";
import Box from "@material-ui/core/Box";
import {makeStyles} from "@material-ui/styles";
import UploadsTable from './Components/UploadsTable';
import AnalysisTable from './Components/AnalysisTable';

const useStyles = makeStyles({});

export default function Admin(props) {
    const [isLoading, setIsLoading] = React.useState(undefined);
    const [statistics, setStatistics] = React.useState(undefined);
    const [filesInput, setFilesInput] = React.useState(undefined);
    const [lastExecution, setLastExecution] = React.useState(undefined);
    const [lastUploads, setLastUploads] = React.useState(undefined);

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
        const statsResponse = await statsData.json();
        handleGetStatistics(statsResponse);

        const lastUploads = await fetch("/api/get_last_runs",
            {
                method: 'GET',
                headers: {
                    'Authorization': 'Bearer ' + props.access_token,
                },
            });
        const lastUploadsResponse = await lastUploads.json();
        setLastUploads(lastUploadsResponse);

        setIsLoading(false);
    };

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
    };

    const handleGetStatistics = (statsResponse) => {
        if (statsResponse !== 'executing') {
            setStatistics(_.toPairsIn(statsResponse.stats));
            setLastExecution(statsResponse.executionTime)

        } else {
            setStatistics(statsResponse);
        }
    };

    return (
        <Container>
            <Box display="flex" justifyContent="center" pb={3}>
                <Typography variant={"h2"}>Admin Portal</Typography>
            </Box>
            {isLoading === true
                ?   <Backdrop open={true}>
                        <CircularProgress size={60}/>
                    </Backdrop> 
                :   <Paper elevation={1} style={{"padding": "2em"}}>
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
                                                <Button 
                                                    type="submit" 
                                                    variant="contained" 
                                                    color="primary"
                                                >
                                                    Upload
                                                </Button>
                                            </form>
                                        </CardContent>
                                        {!_.isEmpty(lastUploads) &&
                                            <UploadsTable tableData={lastUploads} />
                                        }
                                    </Paper>
                                </Grid>
                            </Grid>
                            <Grid container item direction="column" spacing={3} sm={6}>
                                <Grid item>
                                    <Paper>
                                        <CardContent>
                                            <Typography variant="h5" style={{ paddingBottom: 5 }}>Run New Analysis</Typography>
                                            <form onSubmit={handleExecute}>
                                                <Button 
                                                    type="submit" 
                                                    variant="contained" 
                                                    color="primary"
                                                >
                                                    Run Data Analysis
                                                </Button>
                                            </form>
                                        </CardContent>
                                        {!_.isEmpty(statistics) && 
                                            <AnalysisTable lastExecution={lastExecution} tableData={statistics} />
                                        }
                                    </Paper>
                                </Grid>
                            </Grid>
                        </Grid>
                    </Paper>
            }
        </Container>
    );
}
