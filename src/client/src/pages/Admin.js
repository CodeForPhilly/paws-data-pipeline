import React, { Component } from 'react';
import {Tabs, Tab, Container, Paper } from "@material-ui/core";
import TabPanel from '../components/TabPanel';
import Grid from '@material-ui/core/Grid';
// import { DataGrid } from '@material-ui/data-grid';
import { withStyles } from '@material-ui/core/styles';
import Divider from '@material-ui/core/Divider';
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

const columns = [
    { field: 'source', headerName: 'ID', width: 70 },
    { field: 'count', headerName: 'First name', width: 130 }
]
class Admin extends Component {
    constructor(props) {
        super(props);
        this.state = {
            activeIndex: 0,
            loading: false,
            loadingCurrentFiles: false,
            loadingStatistics: false,
            statistics: undefined,
            filesInput: undefined,
            fileListHtml: undefined,
            statisticsListHtml: undefined
        }

        this.handleIndexChange = this.handleIndexChange.bind(this);
        this.handleUpload = this.handleUpload.bind(this);
        this.handleExecute = this.handleExecute.bind(this);
        this.handleGetFileList = this.handleGetFileList.bind(this);
        this.handleGetStatistics = this.handleGetStatistics.bind(this);
    }

    componentDidMount(){
        this.handleGetFileList();
        this.handleGetStatistics();
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
        this.setState({loading: true});

        const response = await fetch('/api/execute');
        const result = await response.json();

        this.setState({loading: false});

        return result
    }

    async handleGetStatistics() {
        this.setState({loadingStatistics: true})

        const statsData = await fetch("/api/statistics");
        const statsResponse = await statsData.json();

        this.setState({statistics: statsResponse});

        // this.setState({fileListHtml: _.map(filesResponse, (fileName) => {
        //     return <li key={fileName}> {fileName}</li>
        // })});        
        // this.setState({statisticsListHtml: _.keys(statsResponse, (key) => {
        //     return <li>{key}: {statsResponse[key]}</li>
        // })});
        let stats = _.toPairsIn(statsResponse)

        this.setState({statisticsListHtml: _.map(stats, (stat) => {
            return <li key={stat[0]}>{stat[0]} {stat[1]}</li>
        })});

        console.log("statisticsListHtml", stats);
        // this.setState({statisticsListHtml: stats});
        this.setState({loadingStatistics: false}) 
    }

    async handleGetFileList() {
        this.setState({loadingCurrentFiles: true})

        const filesData = await fetch("/api/listCurrentFiles");
        const filesResponse = await filesData.json();

        // this.setState({fileList: filesResponse});

        this.setState({fileListHtml: _.map(filesResponse, (fileName) => {
            return (<li key={fileName}> {fileName}</li>)
        })});

        console.log("fileListHtml", this.state.fileListHtml);
        //just a UX indication that a new list has been loaded
        //await new Promise(resolve => setTimeout(resolve, 1000));

        this.setState({loadingCurrentFiles: false})
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
        <ul>{this.state.fileListHtml}</ul>

        let currentStatistics = this.state.loadingStatistics === true ?
        <div className={classes.spinner}>
            <CircularProgress />
        </div>
        :
        <ul>{this.state.statisticsListHtml}</ul>

        return (
            <Container>
                <h2>Admin Options</h2>
                <Paper elevation={2} style={{"marginTop":"1em", "padding":"2em"}}>
                    <Grid container spacing={5}>
                        <Grid item>
                            <Tabs value={this.state.activeIndex} onChange={this.handleIndexChange}>
                                <Tab label="Upload" />
                                <Tab label="Download" />
                                <Tab label="Execute" />
                            </Tabs>
                            {currentTabWithState}
                        <Divider orientation="vertical" flexItem />
                        </Grid>
                        <Grid item>
                            <h3>Current Files</h3>
                            {currentListWithState}
                        </Grid>
                        <Grid item>
                            <h3>Current Stats</h3>
                            {currentStatistics}
                        </Grid>
                    </Grid>
                </Paper>
            </Container>
        );
    }
}

export default withStyles(styles)(Admin);