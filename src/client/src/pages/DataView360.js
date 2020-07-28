import React, {useState, useEffect} from 'react';
import { withStyles, makeStyles } from '@material-ui/core/styles';
import { Paper, Typography, Table, TableContainer, TableHead, TableBody, TableRow, TableCell, Container, capitalize} from '@material-ui/core';

import SearchBar from '../components/SearchBar';


const StyledContact = withStyles((theme)=>({
    root:{
        span:{
        fontWeight:600,
        },
    },

}))(Typography);

const StyledTableCell = withStyles((theme)=>({
    head:{
        backgroundColor: theme.palette.grey.A100,
        fontWeight: 600,
    }
}))(TableCell);

const StyledTableRow = withStyles((theme)=>({
    root:{
        '&:nth-of-type(even)':{
            backgroundColor: theme.palette.action.hover,
        }
    }
}))(TableRow);

/* --------------------------------------------------------/
    Returns Div with Name, Address, Phone, Email, and a
    Summary of the person
/---------------------------------------------------------*/
function ContactInfo(props){

    // Helper function to create labels for each Contact Value
    function BoldLabel(props){
        return (
            <span style={{'fontWeight':'600'}}>
                {props.value}{':\t'}
            </span>
        ) 
    };

    return (
    <Container>
        <Typography align='center' gutterBottom='true' variant='h4'>Contact Info</Typography>
        <Paper variant='outlined' style={{padding:'1em'}}>
        <div style={{"display":"flex", "justifyContent":"space-between"}}>
            <Typography>
                <BoldLabel value="Name" />
                <span>
                    {props.participant.first_name}{'\t'}
                    {props.participant.last_name}
                </span>
            </Typography>
            <StyledContact>
                <BoldLabel value="Phone" />
                <span>
                    {props.participant.phone}
                </span>
            </StyledContact>
            <Typography>
                <BoldLabel value="Email" />
                <span>
                    {props.participant.email}
                </span>
            </Typography>
        </div>
        <Typography>
            <BoldLabel value="Address" />
            <span style={{"textTransform":"uppercase"}}>
                {props.participant.mailing_street}{',\t'}
                {props.participant.mailing_city}{'\t'}
            </span>
        </Typography>
        <Typography>
            <BoldLabel value="Summary" />
            <span>{props.summary}</span>
        </Typography>
        </Paper>
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
    
    function createRow(pet){
        return( <StyledTableRow>
                    <TableCell align="center">{pet.animal_name}</TableCell>
                    <TableCell align="center">{pet.animal_type}</TableCell>
                    <TableCell align="center">{pet.primary_breed}</TableCell>
                    <TableCell align="center">{pet.animal_id}</TableCell>
                    <TableCell align="center">{pet.outcome_date}</TableCell>
                    <TableCell align="center">{pet.age_group}</TableCell>
                </StyledTableRow>);
    }
    return (
        <Container style={{"marginTop":"1em"}}>
            <Typography align='center' gutterBottom='true' variant='h4'>Adoption/Foster Records</Typography> 
            <TableContainer style={{"marginTop":"1em"}} component={Paper} variant='outlined'>
                <Table>
                    <TableHead>
                        <TableRow>
                            <StyledTableCell align="center">Name</StyledTableCell>
                            <StyledTableCell align="center">Type/Species</StyledTableCell>
                            <StyledTableCell align="center">Primary Breed</StyledTableCell>
                            <StyledTableCell align="center">Animal-Number</StyledTableCell>
                            <StyledTableCell align="center">Date of Adoption</StyledTableCell>
                            <StyledTableCell align="center">Current Age</StyledTableCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        { props.adoptions && createRow(props.adoptions) }
                    </TableBody>
                </Table>
           </TableContainer>
        </Container>
    );
}

/*---------------------------------------------------------/ 
    Returns most recent donations [Date, Amount, Campaign]
    Top 5 Button, and More buttons for extended info
/---------------------------------------------------------*/
function Donations(props){

    function createRow(item){
        return( <StyledTableRow>
                    <TableCell align="center">{item.date}</TableCell>
                    <TableCell align="center">{item.amount}</TableCell>
                    <TableCell align="center">{item.type}</TableCell>
                </StyledTableRow>);
    }

    return (
        <Container style={{"marginTop":"1em"}}>
            <Typography align='center' gutterBottom='true' variant='h4'>Donation Records</Typography> 
            <TableContainer style={{"marginTop":"1em"}} component={Paper} variant='outlined'>
                <Table>
                    <TableHead>
                        <TableRow>
                            <StyledTableCell align="center">Date of Donation</StyledTableCell>
                            <StyledTableCell align="center">Amount</StyledTableCell>
                            <StyledTableCell align="center">Campaign Type</StyledTableCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        { props.donations && props.donations.map(i=>createRow(i)) }
                    </TableBody>
                </Table>
            </TableContainer>
        </Container>
    );
}

function Volunteer(props){

    function createRow(item){
        return( <StyledTableRow>
                    <TableCell align="center">{item.start_date}</TableCell>
                    <TableCell align="center">{item.hours}</TableCell>
                    <TableCell align="center">{item.ytd}</TableCell>
                </StyledTableRow>);
    }

    return (
        <Container style={{"marginTop":"1em"}}>
            <Typography align='center' gutterBottom='true' variant='h4'>Volunteer Records</Typography> 
            <TableContainer style={{"marginTop":"1em"}} component={Paper} variant='outlined'>
                <Table>
                    <TableHead>
                        <TableRow>
                            <StyledTableCell align="center">Volunteer activity start</StyledTableCell>
                            <StyledTableCell align="center">Life hours</StyledTableCell>
                            <StyledTableCell align="center">YTD hours</StyledTableCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        { props.volunteer && createRow(props.volunteer) }
                    </TableBody>
                </Table>
            </TableContainer>
        </Container>
    );
}

// Add scoll list of contacts endpoint "/contacts/<search_sub_string>"
//Need to add clinic and volunteer info too
function Dataview(props){

    const [participant, setParticipant] = useState(null);
    const [activeParticipant, setActiveParticipant] = useState(0);
    const handleParticipantChange = (event)=>{
        event.preventDefault();
        setActiveParticipant(event.target.value);
    };

    useEffect(()=>{
        fetch('/360/'+activeParticipant)
            .then(response => response.json())
            .then(response => setParticipant(response))
            .catch(error => console.log(error))
    },[activeParticipant]);

    return(
    <Container>
        <SearchBar activeParticipant={activeParticipant}
            setActiveParticipant={setActiveParticipant}
            handleParticipantChange={handleParticipantChange}/>
        {participant &&
        <Paper elevation={1} style={{"padding":"1em"}}>
            <ContactInfo participant={participant.salesforcecontacts} /> 
            <Donations donations={[{date:"June 01, 1900", amount:"123", type:"FAKE-DONATION"}]} /> 
            <Adoption adoptions={participant.petpoint} />
            <Volunteer />
        </Paper>}
    </Container>
    
    );
}


export default Dataview;