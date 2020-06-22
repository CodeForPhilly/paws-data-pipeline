import React, {useState} from 'react';
import { Paper, Typography, Select, InputLabel, MenuItem, FormControl, TextField, IconButton, Button, Container} from '@material-ui/core';
import Skeleton from '@material-ui/lab/Skeleton';
import SearchIcon from '@material-ui/icons/Search';


/* --------------------------------------------------------/
    Returns Div with Name, Address, Phone, Email, and a
    Summary of the person
/---------------------------------------------------------*/
function ContactInfo(props){

    return (
    <Container>
        <Typography align='center' gutterBottom='true' variant='h4'>Contact Info</Typography>
        <div style={{"display":"flex", "justifyContent":"space-between"}}>
            <Typography>Name: {props.name}</Typography>
            <Typography>Phone: {props.phone}</Typography>
            <Typography>Email: {props.email}</Typography>
        </div>
        <Typography>Address: {props.address}</Typography>
        <Typography>Summary: {props.summary}</Typography>
    </Container>
    );
}

/*---------------------------------------------------------/ 
    Returns most recent donations [Date, Amount, Campaign]
    Top 5 Button, and More buttons for extended info
/---------------------------------------------------------*/
function Donations(props){

    const donations = props.donation ? 
        (<tbody>
            {props.donation.map((i)=>
                <tr>
                    <td>{i.name}</td>
                    <td>{i.amount}</td>
                    <td>{i.campaign}</td>
                </tr>
            )}
        </tbody>) :
        <tbody>
            <tr>
                <td><Skeleton height={100} width={100} > Not Found </Skeleton></td>
                <td><Skeleton height={100} width={100} > Not Found </Skeleton></td>
                <td><Skeleton height={100} width={100} > Not Found </Skeleton></td>
            </tr>
        </tbody>;

    return (
        <Container style={{"marginTop":"1em"}}>
        <Typography align='center' gutterBottom='true' variant='h4'>Donation Records</Typography> 
        <table>
            <thead>
                <tr>
                    <th>Date</th>
                    <th>Amount</th>
                    <th>Campaign</th>
                </tr>
            </thead>
            {donations}
        </table>
        </Container>

    );
}


/*----------------------------------------------------------/
    This will need to transform to a seach bar.

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
        <Container style={{"marginTop":"1em"}}>
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
        </Container>
    );
}


/*--------------------------------------------------------/
    Returns the foster/adoption records for viewing and a hyperlink
    to Petpoint.

    Fields:
        Name, Type/Species, Primary Breed,  A-Number, 
        Date of Adoption, Current Age
/-------------------------------------------------------*/
function Adoption(props){
    
    return (
        <Container style={{"marginTop":"1em"}}>
            <Typography align='center' gutterBottom='true' variant='h4'>Adoption/Foster Records</Typography> 
            <Typography>Name: {props.name}</Typography>
            <Typography>Type/Species: {props.type}</Typography>
            <Typography>Primary Breed: {props.breed}</Typography>
            <Typography>Animal-Number: {props.number}</Typography>
            <Typography>Date of Adoption: {props.adoptionDate}</Typography>
            <Typography>Current Age: {props.age}</Typography>
        </Container>
    );
}

// Add scoll list of contacts endpoint "/salesforcecontacts"
//Need to add clinic and volunteer info too
function Dataview(args){

    const [participant, setParticipant] = useState(null);
    const [participantList, setParticipantList] = useState(null);
    const [participantSearch, setParticipantSearch] = useState(null);

    const handleParticipantChange = (event)=>{
        event.preventDefault();
        setParticipant(event.target.value);
        console.log(participant);
    }

    const handleSubmit = (event)=>{
        event.preventDefault();
        console.log(participantSearch);
        // add search bar and submit text from search bar to endpoint
        fetch('/contacts/'+participantSearch)
            .then(response => response.json())
            .then(response => setParticipantList(response.result))
            .catch(error => console.log(error));
    };

    

    return(
    <Container>
        <Paper elevation={2} style={{"padding":"1em","marginTop":"1em","marginBottom":"1em", "minWidth":"100"}}>
            <div style={{"display":"flex", "minWidth":"100", "justifyContent":"space-between"}}>
                <Typography>Participant Lookup:</Typography>
                <form onSubmit={handleSubmit} style={{"display":"flex"}}>
                    <TextField 
                        id="participant-search" 
                        label="search name"
                        value={participantSearch}
                        variant="outlined"
                        onChange={ (event)=>{setParticipantSearch(event.target.value)}} />
                    <button type="submit">
                        <IconButton component="span">
                            <SearchIcon />
                        </IconButton>
                    </button>
                </form>
                <SelectParticipant handleChange={handleParticipantChange} participantList={participantList} />
            </div>
        </Paper>
        <Paper elevation={2} style={{"padding":"1em"}}>
            <ContactInfo name="mike" address="123 Fake Blvd, Philadelphia, PA" phone="(123) 456-7890" email="a@a.com" summary="ss"/> 
            <Donations donation={[{"name":"mike", "amount":"$1M", "campaign":"Paws4life"}]} />
            <Adoption name="Lola" type="feline" breed="short-hair" number="8675309" adoptionDate="5/1/20" age="2 months" /> 
        </Paper>
    </Container>
    
    );
}


export default Dataview;