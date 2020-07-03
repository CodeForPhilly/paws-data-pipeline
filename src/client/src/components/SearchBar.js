import React, {useState} from 'react';
import { Paper, Select, InputLabel, MenuItem, FormControl, TextField, IconButton} from '@material-ui/core';
import SearchIcon from '@material-ui/icons/Search';

function SearchParticipant(props){
        
    return (
        <div>
            <form onSubmit={props.handleSubmit} style={{"display":"flex"}}>
                <TextField 
                    id="participant-search" 
                    label="search name"
                    value={props.participantSearch}
                    variant="outlined"
                    onChange={ (event)=>{props.setParticipantSearch(event.target.value)}} />
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

    return (
            <FormControl style={{"minWidth":"20em"}}>
                <InputLabel id="paws-participant-label">Select Participant</InputLabel>
                <Select
                    labelId="paws-participant-label"
                    id="paws-participant-select"
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
            .then(response => setParticipantList(response.result))
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
                participantList={participantList}
            />
        </Paper>
    )

}

export default SearchBar;