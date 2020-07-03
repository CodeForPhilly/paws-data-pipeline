import React, {useState, useEffect} from 'react';
import { withStyles, makeStyles } from '@material-ui/core/styles';
import { Paper, Typography, Table, TableContainer, TableHead, TableBody, TableRow, TableCell, Container} from '@material-ui/core';
import Skeleton from '@material-ui/lab/Skeleton';

import SearchBar from '../components/SearchBar';


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

    return (
    <Container>
        <Typography align='center' gutterBottom='true' variant='h4'>Contact Info</Typography>
        <div style={{"display":"flex", "justifyContent":"space-between"}}>
            <Typography>Name: 
                        {props.participant.first_name}{', '}
                        {props.participant.last_name}
            </Typography>
            <Typography>Phone: {props.participant.phone}</Typography>
            <Typography>Email: {props.participant.email}</Typography>
        </div>
        <Typography>Address: 
                    {props.participant.mailing_street}{'\t'}
                    {props.participant.mailing_city}{',\t'}
        </Typography>
        <Typography>Summary: {props.summary}</Typography>
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
            <TableContainer style={{"marginTop":"1em"}}>
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
            <TableContainer style={{"marginTop":"1em"}}>
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
            <TableContainer style={{"marginTop":"1em"}}>
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
    const handleParticipantChange = (event)=>{
        event.preventDefault();
        //setParticipant(event.target.value);

        fetch('/360/'+event.target.value)
            .then(response => response.json())
            .then(response => setParticipant(response))
            .catch(error => console.log(error))
    }

    useEffect(()=>{
        console.log(participant);
    },[participant]);

    return(
    <Container>
        <SearchBar handleParticipantChange={handleParticipantChange}/>
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