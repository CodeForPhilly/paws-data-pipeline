import React from 'react';
import {
    Box,
    Grid,
    Paper,
    Container,
    Typography,
} from "@material-ui/core";

import _ from 'lodash';
import {Alert} from "@material-ui/lab";
import UploadBox from './Components/UploadBox';
import AnalysisBox from './Components/AnalysisBox';
import Loading from './Components/Loading';
import useAlert from '../../hooks/useAlert';

export default function Admin(props) {
    const [isLoading, setIsLoading] = React.useState(undefined);
    const [statistics, setStatistics] = React.useState(undefined);
    const [filesInput, setFilesInput] = React.useState(undefined);
    const [lastExecution, setLastExecution] = React.useState(undefined);
    const [lastUploads, setLastUploads] = React.useState(undefined);
    const [loadingText, setLoadingText] = React.useState("");
    const { setAlert } = useAlert();

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

        setLoadingText("");
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

        try {
            await fetch("/api/file", {
                method: "POST",
                body: formData,
                headers: {
                    Authorization: "Bearer " + props.access_token,
                },
            });

            setAlert({
                type: "success",
                text: `${files.length === 1 ? "1 file" : files.length + " files"} uploaded successfully`,
            });
        } catch (error) {
            console.warn(error);
            setAlert({ type: "error", text: error });
        }

        setFilesInput(undefined);

        await refreshPage();
    };

    const handleExecute = async (event) => {
        event.preventDefault();
        setLoadingText("This may take a few minutes")
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
                ?   <Loading text={loadingText} />
                :   <Paper elevation={1} style={{"padding": "2em"}}>
                        {statistics === 'Running' && <Alert severity="info">Execution is in Progress...</Alert>}
                        <Grid container spacing={5} direction="row" style={{ padding: 16 }}>
                            <UploadBox filesInput={filesInput} handleUpload={handleUpload} lastUploads={lastUploads} />
                            <AnalysisBox handleExecute={handleExecute} lastExecution={lastExecution} statistics={statistics} />
                        </Grid>
                    </Paper>
            }
        </Container>
    );
}
