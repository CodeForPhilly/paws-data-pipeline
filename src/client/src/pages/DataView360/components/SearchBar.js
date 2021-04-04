import React, {Component} from 'react';
import {Button, Paper, MenuItem, TextField, IconButton, Grid} from '@material-ui/core';
import SearchIcon from '@material-ui/icons/Search';
import styles from "./styles/SearchBar.module.css";
import CircularProgress from '@material-ui/core/CircularProgress';

import _ from 'lodash';

const LIST_LIMIT = 200;

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
        this.selectParticipant = this.selectParticipant.bind(this);

    }

    handleParticipantKeyStroke(event) {
        let searchStr = _.get(event, 'target.value');

        if (_.isEmpty(searchStr) !== true) {
            const searchStrSplitted = searchStr.split(' ');
            let shouldShowAlert = false;

            if (_.size(searchStrSplitted) === 2) {
                shouldShowAlert = _.size(searchStrSplitted[0]) < 3 || _.size(searchStrSplitted[1]) < 3;
            } else if (_.size(searchStrSplitted) === 1) {
                shouldShowAlert = _.size(searchStrSplitted[0]) < 3;
            }

            this.setState({alertMinChars: shouldShowAlert});
        }
        this.setState({participantSearch: searchStr});
    }

    searchParticipant(event) {
        return (
            <form onSubmit={this.handleParticipantSearch}>
                <TextField style={{minWidth: 1000}}
                           error={this.state.alertMinChars}
                           helperText={this.state.alertMinChars ? "Requires 3 search characters for first and last name" : ""}
                           id="participant-search"
                           label="Search by First, Last or Full Name"
                           value={this.state.participantSearch}
                           variant="outlined"
                           onChange={this.handleParticipantKeyStroke}/>
                <Button
                    type="submit"
                    disabled={this.state.alertMinChars}
                >
                    <IconButton component="span">
                        <SearchIcon/>
                    </IconButton>
                </Button>
            </form>
        );
    }

    selectParticipant() {
        if (this.state.participantList != null) {
            const participantList = this.state.participantList.slice(0, LIST_LIMIT);

            _.map(participantList, person => {
                return (<MenuItem value={person.contact_id} key={person.contact_id}>
                    {person.name}
                    {" "}
                    ({person.email})
                </MenuItem>)
            });
        }

        return (
            <div></div>
        );
    }

    async handleParticipantSearch(event) {
        event.preventDefault();
        if (_.isEmpty(this.state.participantSearch) !== true) {
            this.props.handleSearchChange(this.state.participantSearch);
        }
    };

    render() {
        return (
            <Grid container>
                <Grid container
                      direction="row"
                      justify="center"
                      alignItems="center">
                    <h1>PAWS Contact Search</h1>
                </Grid>
                <Paper className={styles.search_bar} elevation={1} style={{
                    "display": "flex",
                    "padding": "1em",
                    "justifyContent": "space-around"
                }}>
                    {this.searchParticipant()}
                    {this.state.isSearchBusy === true ?
                        <CircularProgress/> : this.selectParticipant()}
                </Paper>
            </Grid>
        )
    }
}

export default SearchBar;