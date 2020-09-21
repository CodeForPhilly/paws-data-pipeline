import React, { Component } from 'react';
import {Button, Paper, Select, InputLabel, MenuItem, FormControl, TextField, IconButton} from '@material-ui/core';
import SearchIcon from '@material-ui/icons/Search';
import { withStyles } from '@material-ui/core/styles';
import CircularProgress from '@material-ui/core/CircularProgress';

import _ from 'lodash';

const LIST_LIMIT = 200;

const styles = theme => ({
    spinner: {
        display: 'flex',
        marginLeft: theme.spacing(2)
    }
});

class SearchBar extends Component {
    constructor(props) {
        super(props);

        this.state = {
            alertMinChars: true,
            participantList: [],
            participantSearch: '',
            isSearchBusy: false
        }

        this.handleParticipantSearch = this.handleParticipantSearch.bind(this);
        this.handleParticipantKeyStroke = this.handleParticipantKeyStroke.bind(this);
        this.selectParticipant = this.selectParticipant.bind(this);

    }

    handleParticipantKeyStroke(event) {
        let searchStr = _.get(event, 'target.value');

        if(_.isEmpty(searchStr) !== true) {
            const searchStrSplitted = searchStr.split(' ');
            let shouldShowAlert = false;

            if(_.size(searchStrSplitted) === 2) {
                shouldShowAlert = _.size(searchStrSplitted[0]) < 3 || _.size(searchStrSplitted[1]) < 3;
            }
            else if (_.size(searchStrSplitted) === 1) {
                shouldShowAlert = _.size(searchStrSplitted[0]) < 3;
            }

            this.setState({alertMinChars: shouldShowAlert});
        }
        this.setState({participantSearch: searchStr});
    }

    searchParticipant(event) {
        return (
                <form onSubmit={this.handleParticipantSearch} style={{"display":"flex"}}>
                    <TextField style={{"min-width":"300px"}}
                        error={this.state.alertMinChars}
                        helperText={this.state.alertMinChars ? "Requires 3 search characters for first and last name" : ""}
                        id="participant-search"
                        label="Search by First or Full name(first last)"
                        value={this.state.participantSearch}
                        variant="outlined"
                        onChange={this.handleParticipantKeyStroke} />
                    <Button
                        type="submit"
                        disabled={this.state.alertMinChars}
                        >
                        <IconButton component="span">
                            <SearchIcon />
                        </IconButton>
                    </Button>
                </form>
        );
    }

    selectParticipant(){
        let participants;

        if(this.state.participantList != null) {
            const participantList = this.state.participantList.slice(0,LIST_LIMIT);

            participants = _.map(participantList, person => {
                return (<MenuItem value={person.contact_id} key={person.contact_id}>
                    {person.name}
                    {" "}
                    ({person.email})
                </MenuItem>)
            });
        }

        return (
            <FormControl style={{"minWidth":"20em"}}>
                <InputLabel id="paws-participant-label">Select Participant - Top 200 Results</InputLabel>
                <Select
                    labelId="paws-participant-label"
                    id="paws-participant-select"
                    value={this.props.participant}
                    onChange={this.props.handleParticipantChange}
                    defaultValue={'DEFAULT'}
                >
                    <MenuItem value="DEFAULT" key="DEFAULT" disabled>Choose a Participant ...</MenuItem>
                    {participants}
                    </Select>
            </FormControl>
        );
    }

    async handleParticipantSearch(event) {
        if(_.isEmpty(this.state.participantSearch) !== true) {
            event.preventDefault();
            this.setState({isSearchBusy: true});

            await new Promise(resolve => setTimeout(resolve, 1000));
            let response = await fetch(`/api/contacts/${this.state.participantSearch}`);
            response = await response.json();

            this.setState({participantList: response.result})
            this.props.handleSearchChange();

            this.setState({isSearchBusy: false});
        }
    };

    render() {
        const { classes } = this.props;

        return (
            <Paper elevation={1} style={{
                    "display":"flex",
                    "padding":"1em",
                    "margin":"1em 0 1em 0",
                    "minWidth":"100",
                    "justifyContent":"space-around"
                }}>
                {this.searchParticipant()}


                {this.state.isSearchBusy === true ?
                (<div className={classes.spinner}>
                    <CircularProgress />
                </div>) : this.selectParticipant()}
            </Paper>
        )
    }
}

export default withStyles(styles)(SearchBar);