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
    Table
} from "@material-ui/core";

import {withStyles} from '@material-ui/core/styles';
import _ from 'lodash';
import moment from "moment";
import {Alert} from "@material-ui/lab";

const styles = theme => ({
    root: {
        margin: theme.spacing(2),
    },
    backdrop: {
        zIndex: theme.zIndex.drawer + 1,
        color: '#fff',
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
            }})

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
                method: 'GET',
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
        const {classes} = this.props;

        return (
            <div className={classes.root}>
                <h1>Admin Portal</h1>
                {this.state.statistics === 'Running' && <Alert severity="info">Execution is in Progress...</Alert>}
                <Backdrop className={classes.backdrop} open={this.state.isLoading !== false}>
                    <CircularProgress size={60}/>
                </Backdrop>
                <Grid container spacing={3} direction="column" style={{padding: 20}}>
                    <Grid container spacing={3} direction="row">
                        <Grid item sm={6}>
                            <h2>Latest Files</h2>
                            {_.isEmpty(this.state.fileListHtml) !== true &&
                            <TableContainer component={Paper} className="statisticsData">
                                <Table aria-label="simple table" className={classes.table}>
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
                                            let fileDateFormatted = moment.utc(fileDateOnlyNumbers, "YYYYMMDDhmmss").local().format("MMMM Do YYYY, h:mm:ss a");

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

                            <Paper style={{padding: 5, marginTop: 10}}>
                                <CardContent>
                                    <h3 style={{marginTop: 0}}>Upload Files</h3>
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

                        <Grid item sm={6}>
                            <h2> Last Match Analysis </h2>
                            {_.isEmpty(this.state.statistics) !== true &&
                            this.state.statistics !== 'Running' &&
                            <TableContainer component={Paper} className="statisticsData">
                                <Table aria-label="simple table" className={classes.table}>
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
                            <Paper style={{padding: 5, marginTop: 10}}>
                                <CardContent>
                                    <h3 style={{marginTop: 0}}>Run New Analysis</h3>
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
            </div>
        );
    }
}

export default withStyles(styles)(Admin);