import React, { Component } from 'react';
import {Tabs, Tab, Container, Paper } from "@material-ui/core";
import TabPanel from '../components/TabPanel';
import Grid from '@material-ui/core/Grid';
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

class Admin extends Component {
    constructor(props) {
        super(props);
        this.state = {
            activeIndex: 0,
            loading: false,
            loadingCurrentFiles: false,
            fileList: undefined,
            filesInput: undefined,
            fileListHtml: undefined
        }

        this.handleIndexChange = this.handleIndexChange.bind(this);
        this.handleUpload = this.handleUpload.bind(this);
        this.handleExecute = this.handleExecute.bind(this);
        this.handleGetFileList = this.handleGetFileList.bind(this);
    }

    componentDidMount(){
        this.handleGetFileList();
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

    async handleGetFileList() {
        this.setState({loadingCurrentFiles: true})

        const filesData = await fetch("/api/listCurrentFiles");
        const filesResponse = await filesData.json();

        this.setState({fileList: filesResponse});

        this.setState({fileListHtml: _.map(filesResponse, (fileName) => {
            return <li>{fileName}</li>
        })});

        //just a UX indication that a new list has been loaded
        await new Promise(resolve => setTimeout(resolve, 1000));

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
                    </Grid>
                </Paper>
            </Container>
        );
    }
}

export default withStyles(styles)(Admin);