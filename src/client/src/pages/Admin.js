import React, {Component} from 'react';
import {Paper, Button, TableHead} from "@material-ui/core";
import Grid from '@material-ui/core/Grid';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableContainer from '@material-ui/core/TableContainer';
import TableRow from '@material-ui/core/TableRow';
import {withStyles} from '@material-ui/core/styles';
import CircularProgress from '@material-ui/core/CircularProgress';
import _ from 'lodash';
import CardContent from "@material-ui/core/CardContent";
import moment from "moment";


const styles = theme => ({
    loader: {
        marginTop: "40px"
    },
    spinner: {
        marginLeft: theme.spacing(2),
        display: 'flex', justifyContent: 'center', position: 'absolute', left: '50%', top: '50%',
        transform: 'translate(-50%, -50%)'
    }
});

const StyledTableCell = withStyles((theme) => ({
    head: {
        backgroundColor: 'initial', // here
        fontWeight: 600,
    }
}))(TableCell);

const StyledTableRow = withStyles((theme) => ({
    root: {
        '&:nth-of-type(even)': {
            backgroundColor: 'initial', // and here
        }
    }
}))(TableRow);


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

        var formData = new FormData();

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
                {this.state.isLoading === true ?
                    <div className={classes.spinner}>
                        <CircularProgress size={60}/>
                    </div>
                    :
                    <Grid container spacing={3} direction="column" style={{padding: 30}}>
                        <Grid container spacing={3} direction="row">
                            <Grid item sm={6}>
                                <h2>Latest Files</h2>
                                {_.isEmpty(this.state.fileListHtml) !== true &&
                                <TableContainer component={Paper} className="statisticsData">
                                    <Table aria-label="simple table" className={classes.table}>
                                        <TableHead>
                                            <TableRow>
                                                <StyledTableCell>File Type</StyledTableCell>
                                                <StyledTableCell>Last Updated</StyledTableCell>
                                            </TableRow>
                                        </TableHead>
                                        <TableBody>
                                            {_.map(this.state.fileListHtml, file => {
                                                const fileName = file.split("-")[0];
                                                let fileDate = file.split("-").slice(1).join().split(".")[0];
                                                let fileDateOnlyNumbers = fileDate.replaceAll(",", "");
                                                let fileDateFormatted = moment(fileDateOnlyNumbers, "YYYYMMDDhmmss").format("MMMM Do YYYY, h:mm:ss a");

                                                return (
                                                    <StyledTableRow>
                                                        <TableCell>{fileName}</TableCell>
                                                        <TableCell>{fileDateFormatted}</TableCell>
                                                    </StyledTableRow>
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
                                                    Last Analysis
                                                </TableCell>
                                                <TableCell align="left">
                                                    {moment(this.state.lastExecution, "dddd MMMM Do h:mm:ss YYYY").local().format("MMMM Do YYYY, h:mm:ss a")}
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

                    </Grid>}
            </div>
        );
    }

}

export default withStyles(styles)(Admin);