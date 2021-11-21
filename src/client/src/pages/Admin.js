import React, {Component} from 'react';
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

import {withStyles} from '@material-ui/core/styles';
import _ from 'lodash';
import moment from "moment";
import {Alert} from "@material-ui/lab";
import Box from "@material-ui/core/Box";

const styles = theme => ({
    root: {
        margin: theme.spacing(2),
    }
});

class Admin extends Component {
    constructor(props) {
        super(props);
        this.state = {
            activeIndex: 0,
            isLoading: undefined,
            statistics: undefined,
            filesInput: undefined,
            fileListHtml: undefined,
            lastExecution: undefined,
            serverBusy: false
        }

        this.handleIndexChange = this.handleIndexChange.bind(this);
        this.handleUpload = this.handleUpload.bind(this);
        this.handleExecute = this.handleExecute.bind(this);
        this.handleGetFileList = this.handleGetFileList.bind(this);
        this.handleGetStatistics = this.handleGetStatistics.bind(this);
    }

    async refreshPage() {
        this.setState({isLoading: true})

        await this.handleGetFileList();
        await this.handleGetStatistics();

        await this.setState({isLoading: false})
    }

    componentDidMount() {
        this.refreshPage();
    }

    handleIndexChange(event, newIndex) {
        this.setState({activeIndex: newIndex});
    };

    async handleUpload(event) {
        event.preventDefault();

        this.setState({isLoading: true});

        let formData = new FormData();

        let files = _.get(event, 'target.[0].files');
        _.forEach(files, element => {
            formData.append('file', element, element.name)
        })

        await fetch("/api/file", {
            method: 'POST',
            body: formData,
            headers: {
                'Authorization': 'Bearer ' + this.props.access_token
            }
        })

        await this.handleGetFileList();

        await this.setState({
            isLoading: false,
            filesInput: undefined
        });

        await this.refreshPage()
    };

    async handleExecute(event) {
        event.preventDefault();

        this.setState({isLoading: true});

        await fetch('/api/execute',
            {
                method: 'POST',
                headers: {
                    'Authorization': 'Bearer ' + this.props.access_token
                }
            });

        this.refreshPage();
    }

    async handleGetStatistics() {
        const statsData = await fetch("/api/statistics",
            {
                method: 'GET',
                headers: {
                    'Authorization': 'Bearer ' + this.props.access_token
                }
            });
        const statsResponse = await statsData.json()

        if (statsResponse !== 'executing') {
            this.setState({
                statistics: _.toPairsIn(statsResponse.stats),
                lastExecution: statsResponse.executionTime
            });
        } else {
            this.setState({statistics: statsResponse});
        }
    }

    async handleGetFileList() {
        const filesData = await fetch("/api/listCurrentFiles",
            {
                method: 'GET',
                headers: {
                    'Authorization': 'Bearer ' + this.props.access_token
                }
            });
        const filesResponse = await filesData.json();
        this.setState({fileListHtml: filesResponse});
    }

    render() {
        return (
            <Container>
                <Box display="flex" justifyContent="center" pb={3}>
                    <Typography variant={"h2"}>Admin Portal</Typography>
                </Box>
                <Paper elevation={1} style={{"padding": "2em"}}>
                    {this.state.statistics === 'Running' && <Alert severity="info">Execution is in Progress...</Alert>}
                    <Backdrop open={this.state.isLoading !== false}>
                        <CircularProgress size={60}/>
                    </Backdrop>
                    <Grid container item spacing={5} direction="row" style={{padding: 20}}>
                        <Grid container item direction="column" spacing={3} sm={6}>
                            <Grid item>
                                <Typography variant="h5">Latest Files</Typography>
                            </Grid>
                            <Grid item>
                                {_.isEmpty(this.state.fileListHtml) !== true &&
                                <TableContainer component={Paper}>
                                    <Table aria-label="simple table">
                                        <TableHead>
                                            <TableRow>
                                                <TableCell><b>File Type</b></TableCell>
                                                <TableCell><b>Last Updated</b></TableCell>
                                            </TableRow>
                                        </TableHead>
                                        <TableBody>
                                            {_.map(this.state.fileListHtml, (file, index) => {
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
                                </TableContainer>}
                            </Grid>
                            <Grid item>
                                <Paper>
                                    <CardContent>
                                        <Typography variant="h5">Upload Files</Typography>
                                        <form onSubmit={this.handleUpload}>
                                            <input type="file" value={this.state.filesInput} multiple/>
                                            <Button type="submit" variant="contained" color="primary"
                                                    disabled={this.state.statistics === 'Running'}>
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


                            {_.isEmpty(this.state.statistics) !== true &&
                            this.state.statistics !== 'Running' &&
                            <TableContainer component={Paper}>
                                <Table aria-label="simple table">
                                    <TableBody>
                                        <TableRow key='time'>
                                            <TableCell align="left" component="th" scope="row">
                                                <b>Last Analysis</b>
                                            </TableCell>
                                            <TableCell align="left">
                                                <b>
                                                    {moment(this.state.lastExecution, "dddd MMMM Do h:mm:ss YYYY").local().format("MMMM Do YYYY, h:mm:ss a")}
                                                </b>
                                            </TableCell>
                                        </TableRow>
                                        {this.state.statistics.map((row, index) => (
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
                                        <Typography variant="h5">Run New Analysis</Typography>
                                        <form onSubmit={this.handleExecute}>
                                            <Button type="submit" variant="contained" color="primary"
                                                    disabled={this.state.statistics === 'Running'}>
                                                Run Data Analysis
                                            </Button>
                                        </form>
                                    </CardContent>
                                </Paper>
                            </Grid>

                        </Grid>
                    </Grid>
                </Paper>
            </Container>
        );
    }
}

export default withStyles(styles)(Admin);