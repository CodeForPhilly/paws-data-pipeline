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

const styles = theme => ({
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
            isLoading: false,
            statistics: [],
            filesInput: undefined,
            fileListHtml: undefined,
            lastExecution: undefined
        }

        this.handleIndexChange = this.handleIndexChange.bind(this);
        this.handleUpload = this.handleUpload.bind(this);
        this.handleExecute = this.handleExecute.bind(this);
        this.handleGetFileList = this.handleGetFileList.bind(this);
        this.handleGetStatistics = this.handleGetStatistics.bind(this);
    }

    refreshPage() {
        this.handleGetFileList();
        this.handleGetStatistics();
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

        await fetch("/api/file", {method: 'POST', body: formData})

        await this.handleGetFileList();

        this.setState({isLoading: false});
    };

    async handleExecute(event) {
        event.preventDefault();

        this.setState({isLoading: true});

        const response = await fetch('/api/execute');
        const result = await response.json();

        this.setState({isLoading: false});

        this.refreshPage();

        return result
    }

    async handleGetStatistics() {
        this.setState({isLoading: true})

        try {
            const statsData = await fetch("/api/statistics");
            const statsResponse = await statsData.json();

            this.setState({
                statistics: _.toPairsIn(statsResponse.stats),
                lastExecution: statsResponse.executionTime
            });

            this.setState({isLoading: false})
        } finally {
            this.setState({isLoading: false})
        }

    }

    async handleGetFileList() {
        this.setState({isLoading: true})

        try {
            const filesData = await fetch("/api/listCurrentFiles");
            const filesResponse = await filesData.json();

            this.setState({fileListHtml: filesResponse});

        } finally {
            this.setState({isLoading: false})
        }
    }

    render() {
        const {classes} = this.props;

        return (
            <div style={{paddingLeft: 20}}>
                <h1>Admin Portal</h1>
                    <Backdrop  className={classes.backdrop} open={this.state.isLoading === true}>
                        <CircularProgress size={60}/>
                    </Backdrop>
                    <Grid container spacing={3} direction="column" style={{padding: 30}}>
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
                                            {_.map(this.state.fileListHtml, file => {
                                                const fileName = file.split("-")[0];
                                                let fileDate = file.split("-").slice(1).join().split(".")[0];
                                                let fileDateOnlyNumbers = fileDate.replaceAll(",", "");
                                                let fileDateFormatted = moment(fileDateOnlyNumbers, "YYYYMMDDhmmss").format("MMMM Do YYYY, h:mm:ss a");

                                                return (
                                                    <TableRow>
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
                                            <Button type="submit" variant="contained" color="primary">Upload</Button>
                                        </form>
                                    </CardContent>
                                </Paper>
                            </Grid>

                            <Grid item sm={6}>
                                <h2> Data Analysis </h2>
                                {_.isEmpty(this.state.statistics) !== true &&
                                <TableContainer component={Paper} className="statisticsData">
                                    <Table aria-label="simple table" className={classes.table}>
                                        <TableBody>
                                            <TableRow key='time'>
                                                <TableCell align="left" component="th" scope="row">
                                                    <b>Last Analysis</b>
                                                </TableCell>
                                                <TableCell align="left">
                                                    <b>{moment(this.state.lastExecution, "dddd MMMM Do h:mm:ss YYYY").local().format("MMMM Do YYYY, h:mm:ss a")}</b>
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
                                </TableContainer>}
                                <Paper style={{padding: 5, marginTop: 10}}>
                                    <CardContent>
                                        <h3 style={{marginTop: 0}}>Run New Analysis</h3>
                                        <form onSubmit={this.handleExecute}>
                                            <Button type="submit" variant="contained"
                                                    color="primary">Run Data Analysis</Button>
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