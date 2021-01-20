import React, { Component } from 'react';
import {Tabs, Tab, Paper } from "@material-ui/core";
import TabPanel from '../components/TabPanel';
import Grid from '@material-ui/core/Grid';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableContainer from '@material-ui/core/TableContainer';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import { withStyles } from '@material-ui/core/styles';
import LinearProgress from '@material-ui/core/LinearProgress';
import CircularProgress from '@material-ui/core/CircularProgress';
import { UploadForm, DownloadForm, ExecuteForm } from '../components/Forms';
import _ from 'lodash';


const styles = theme => ({
    loader: {
        marginTop: "40px"
    },
    spinner: {
        display: 'flex',
        marginLeft: theme.spacing(2)
    }
});

class Admin extends Component {
    constructor(props) {
        super(props);
        this.state = {
            activeIndex: 0,
            loading: false,
            loadingCurrentFiles: false,
            loadingStatistics: false,
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

    componentDidMount(){
        this.refreshPage();
    }

    handleIndexChange(event, newIndex){
        this.setState({activeIndex: newIndex});
    };

    async handleUpload(event){
        event.preventDefault();

        this.setState({loading: true});

        var formData = new FormData();

        let files = _.get(event, 'target.[0].files');
        _.forEach(files, element => {
           formData.append('file', element, element.name)
        })

        await fetch("/api/file", { method:'POST', body:formData })

        await this.handleGetFileList();

        this.setState({loading: false});
    };

    async handleExecute(event) {
        event.preventDefault();
        // TODO: it looks like it handles it, but may want to tie events into stats too (like set loadingStatistics: true)
        this.setState({loading: true});

        const response = await fetch('/api/execute');
        const result = await response.json();

        this.setState({loading: false});

        this.refreshPage();

        return result
    }

    async handleGetStatistics() {
        this.setState({loadingStatistics: true})

        try {
            const statsData = await fetch("/api/statistics");
            const statsResponse = await statsData.json();

            this.setState({
                statistics: _.toPairsIn(statsResponse.stats),
                lastExecution: statsResponse.executionTime
            });

            console.log("statisticsListHtml", this.state.statistics);
            // this.setState({statisticsListHtml: stats});
            this.setState({loadingStatistics: false})
        }
        finally {
            this.setState({loadingStatistics: false})
        }

    }

    async handleGetFileList() {
        this.setState({loadingCurrentFiles: true})

        try{
            const filesData = await fetch("/api/listCurrentFiles");
            const filesResponse = await filesData.json();

            // this.setState({fileList: filesResponse});

            this.setState({fileListHtml: _.map(filesResponse, (fileName) => {
                return (<li key={fileName}> {fileName}</li>)
            })});

            console.log("fileListHtml", this.state.fileListHtml);
            //just a UX indication that a new list has been loaded
            //await new Promise(resolve => setTimeout(resolve, 1000));
        }

        finally {
            this.setState({loadingCurrentFiles: false})
        }

    }

    render() {
        const { classes } = this.props;

        let currentTabWithState = this.state.loading === true ?
        <div className={classes.loader}>
            <LinearProgress />
        </div>
        :
        <div>
            <TabPanel value={this.state.activeIndex} index={0}>
              <UploadForm filesInput={this.state.filesInput} handleUpload={this.handleUpload}/>
            </TabPanel>
            <TabPanel value={this.state.activeIndex} index={1}>
              <DownloadForm />
            </TabPanel>
            <TabPanel value={this.state.activeIndex} index={2}>
              <ExecuteForm handleExecute={this.handleExecute}/>
            </TabPanel>
        </div>

        let currentListWithState = this.state.loadingCurrentFiles === true ?
        <div className={classes.spinner}>
            <CircularProgress />
        </div>
        :
        <Paper style={{padding: 5}}>
            <ul>{this.state.fileListHtml}</ul>
        </Paper>

        let currentStatistics = this.state.loadingStatistics === true ?
        <div className={classes.spinner}>
            <CircularProgress />
        </div>
        : _.isEmpty(this.state.statistics) !== true &&
        <TableContainer component={Paper} className="statisticsData">
            <Table aria-label="simple table" className={classes.table}>
                <TableHead>
                    <TableRow>
                        <TableCell>Sources Matched</TableCell>
                        <TableCell align="left">Number of Matches</TableCell>
                    </TableRow>
                </TableHead>
                <TableBody>
                {this.state.statistics.map((row) => (
                    <TableRow key={row[0]}>
                    <TableCell align="left" component="th" scope="row">
                        {row[0]}
                    </TableCell>
                        <TableCell align="left">{row[1]}</TableCell>
                    </TableRow>
                ))}
                </TableBody>
            </Table>
        </TableContainer>

        return (
            <div style={{paddingLeft: 20}}>
                <h2>Admin Portal</h2>
                    <Grid container spacing={3} direction="column"  style={{padding:30}}>
                        <Grid container spacing={3} direction="row">
                            <Grid item sm={5} >
                                <h3>Options</h3>
                                <Paper style={{padding: 5}}>
                                    <Tabs value={this.state.activeIndex} onChange={this.handleIndexChange}>
                                        <Tab label="Upload" />
                                        <Tab label="Download" />
                                        <Tab label="Execute" />
                                    </Tabs>
                                    {currentTabWithState}
                                </Paper>
                            </Grid>
                            <Grid item sm={4}>
                                <h3>Current Files</h3>
                                {currentListWithState}
                            </Grid>
                        </Grid>
                        <Grid container spacing={3} direction="row">
                            <Grid item sm={4}>
                                <h3>Matching Stats from last Execution: {this.state.lastExecution}</h3>
                                {currentStatistics}
                            </Grid>
                        </Grid>
                    </Grid>
            </div>
        );
    }
}

export default withStyles(styles)(Admin);