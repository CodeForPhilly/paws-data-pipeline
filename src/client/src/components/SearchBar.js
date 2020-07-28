import React, {useState} from 'react';
import { Paper, Select, InputLabel, MenuItem, FormControl, TextField, IconButton} from '@material-ui/core';
import {alert, Alert, AlertTitle} from '@material-ui/lab';
import SearchIcon from '@material-ui/icons/Search';


/*------------------------------------------------------/
To Do:
    1. Make sure atleast three chars are entered for a search
    2. Warn user when results are > 200.

/------------------------------------------------------*/
function SearchParticipant(props){
    
    const [alertMinChars, setAlertMinChar]= useState(true);

    const handleChange = (event)=>{
        const strSearch=event.target.value;

        if ((strSearch.length) > 2) {
            setAlertMinChar(false);
            props.setParticipantSearch(strSearch);
        }
        else {
            setAlertMinChar(true);
            props.setParticipantSearch(strSearch)
        }

    }

    

    return (
        <div>
            {alertMinChars ?
            <Alert severity="error">
                <AlertTitle>Error</AlertTitle>
                Minimum number of characters for searching is 3
            </Alert> : <div></div>

            }
            <form onSubmit={props.handleSubmit} style={{"display":"flex"}}>
                <TextField 
                    id="participant-search" x
                    label="search name"
                    value={props.participantSearch}
                    variant="outlined"
                    onChange={handleChange} />
                <button type="submit">
                    <IconButton component="span">
                        <SearchIcon />
                    </IconButton>
                </button>
            </form>
        </div>
    );
}


/*----------------------------------------------------------/
    This will need to transform to a search bar.

    Search substring match.

    Drop down is for the substring match

/---------------------------------------------------------*/
function SelectParticipant(props){

    const participants = props.participantList && 
        props.participantList.map(person =>
        <MenuItem value={person.contact_id}>
            {person.name}
            {" "}
            ({person.email})
        </MenuItem>)

    console.log(props.activeParticipant);
    return (
            <FormControl style={{"minWidth":"20em"}}>
                <InputLabel id="paws-participant-label">Select Participant</InputLabel>
                <Select
                    labelId="paws-participant-label"
                    id="paws-participant-select"
                    value={props.activeParticipant}
                    onChange={props.handleChange}
                    >
                        {participants}
                    </Select>
            </FormControl>
    );
}


/*---------------------------------------------------------/
    Search Bar functionality

    Search for a substring of particpant names
    Select Participant from a drop down menu of matches

/--------------------------------------------------------*/
function SearchBar(props){
    const [participantList, setParticipantList] = useState(null);
    const [participantSearch, setParticipantSearch] = useState(null);
   
    // Submits a request to contacts/<participant sub string> api
    // returns list of matching participants
    const handleSubmit = (event)=>{
        event.preventDefault();
        fetch('/contacts/'+participantSearch)
            .then(response => response.json())
            .then(response => {
                setParticipantList(response.result);
                props.setActiveParticipant(response.result[0].contact_id);
            })
            .catch(error => console.log(error));
    };

    return (
       <Paper elevation={1} style={{
                "display":"flex",
                "padding":"1em",
                "margin":"1em 0 1em 0",
                "minWidth":"100",
                "justifyContent":"space-around"
            }}>
            <SearchParticipant
                handleSubmit={handleSubmit}
                participantSearch={participantSearch}
                setParticipantSearch={setParticipantSearch}
            />
            <SelectParticipant
                handleChange={props.handleParticipantChange}
                activeParticipant={props.activeParticipant}
                participantList={participantList}
            />
        </Paper>
    )

}

export default SearchBar;