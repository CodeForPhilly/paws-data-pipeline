import React, {useState} from 'react';
import {Button, Paper, Select, InputLabel, MenuItem, FormControl, TextField, IconButton} from '@material-ui/core';
import SearchIcon from '@material-ui/icons/Search';

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
            <form onSubmit={props.handleSearch} style={{"display":"flex"}}>
                <TextField
                    error={alertMinChars}
                    helperText={alertMinChars?
                            "Requires 3 search characters":""}
                    id="participant-search" x
                    label="search name"
                    value={props.participantSearch}
                    variant="outlined"
                    onChange={handleChange} />
                <Button 
                    type="submit"
                    disabled={alertMinChars}
                    >
                    <IconButton component="span">
                        <SearchIcon />
                    </IconButton>
                </Button>
            </form>
    );
}


/*----------------------------------------------------------/
    This will need to transform to a search bar.

    Search substring match.

    Drop down is for the substring match

/---------------------------------------------------------*/
function SelectParticipant(props){

    let participants;

    if (props.participantList != null) {
        const participantIndexLimit=200;
        const participantList = props.participantList.slice(0,participantIndexLimit);

        participants =
            participantList.map((person,index) =>
            
            <MenuItem value={person.contact_id}>
                {person.name}
                {" "}
                ({person.email})
            </MenuItem>)

    }

    return (
            <FormControl style={{"minWidth":"20em"}}>
                <InputLabel id="paws-participant-label">Select Participant - Top 200 Results</InputLabel>
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
    const handleSearch = (event)=>{
        event.preventDefault();
        fetch('/api/contacts/'+participantSearch)
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
                handleSearch={handleSearch}
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