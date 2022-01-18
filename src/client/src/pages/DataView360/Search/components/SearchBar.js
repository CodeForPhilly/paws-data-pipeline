import React, {Component} from 'react';
import {Button, TextField, IconButton, Grid, Paper} from '@material-ui/core';
import SearchIcon from '@material-ui/icons/Search';

import _ from 'lodash';
import {withStyles} from "@material-ui/core/styles";

const customStyles = theme => ({
    paper: {
        padding: theme.spacing(2)
    }
});


class SearchBar extends Component {
    constructor(props) {
        super(props);

        this.state = {
            alertMinChars: true,
            participantSearch: '',
            isSearchBusy: false
        }

        this.handleParticipantSearch = this.handleParticipantSearch.bind(this);
        this.handleParticipantKeyStroke = this.handleParticipantKeyStroke.bind(this);

    }

    handleParticipantKeyStroke(event) {
        let searchStr = _.get(event, 'target.value');

        if (_.isEmpty(searchStr) !== true) {
            const searchStrSplitted = searchStr.split(' ');
            let shouldShowAlert = false;

            if (_.size(searchStrSplitted) === 2) {
                shouldShowAlert = _.size(searchStrSplitted[0]) < 2 || _.size(searchStrSplitted[1]) < 2;
            } else if (_.size(searchStrSplitted) === 1) {
                shouldShowAlert = _.size(searchStrSplitted[0]) < 2;
            }

            this.setState({alertMinChars: shouldShowAlert});
        }
        this.setState({participantSearch: searchStr});
    }

    searchParticipant(event) {
        return (

            <form onSubmit={this.handleParticipantSearch}>
                <Grid container directio={"row"} justify="space-between">
                    <Grid item sm={10}>
                        <TextField fullWidth autoFocus
                                   error={this.state.alertMinChars}
                                   helperText={this.state.alertMinChars ? "Requires 3 search characters for first and last name" : ""}
                                   id="participant-search"
                                   label="Search by First, Last or Full Name"
                                   value={this.state.participantSearch}
                                   variant="outlined"
                                   onChange={this.handleParticipantKeyStroke}/>
                    </Grid>
                    <Grid item>
                        <Button type="submit" disabled={this.state.alertMinChars}>
                            <IconButton component="span">
                                <SearchIcon/>
                            </IconButton>
                        </Button>
                    </Grid>
                </Grid>


            </form>
        );
    }

    async handleParticipantSearch(event) {
        event.preventDefault();
        if (_.isEmpty(this.state.participantSearch) !== true) {
            this.props.handleSearchChange(this.state.participantSearch);
        }
    };

    render() {
        const {classes} = this.props;

        return (
            <Grid container direction={"column"}>
                <Grid container direction={"row"} justify={"center"}>
                    <Grid item xs={9}>
                        <Paper className={classes.paper}>
                            {this.searchParticipant()}
                        </Paper>
                    </Grid>
                </Grid>
            </Grid>
        )
    }
}

export default withStyles(customStyles)(SearchBar);