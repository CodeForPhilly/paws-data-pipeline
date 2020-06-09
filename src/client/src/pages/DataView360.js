import React from 'react';
import { Paper, Typography } from '@material-ui/core';
import Skeleton from '@material-ui/lab/Skeleton';

/* --------------------------------------------------------/
    Returns Div with Name, Address, Phone, Email, and a
    Summary of the person
/---------------------------------------------------------*/
function ContactInfo(props){

    return (
    <Paper variant="outlined">
        <Typography>Name: {props.name}</Typography>
        <Typography>Address: {props.address}</Typography>
        <Typography>Phone: {props.phone}</Typography>
        <Typography>Email: {props.email}</Typography>
        <Typography>Summary: {props.summary}</Typography>
    </Paper>
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
                    <td>{i.address}</td>
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
        <Paper variant="outlined">
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
        </Paper>

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
        <div>
            <Typography>Name: {props.name}</Typography>
            <Typography>Type/Species: {props.type}</Typography>
            <Typography>Primary Breed: {props.breed}</Typography>
            <Typography>Animal-Number: {props.number}</Typography>
            <Typography>Date of Adoption: {props.adoptionDate}</Typography>
            <Typography>Current Age: {props.age}</Typography>
        </div>
    );
}


//Need to add clinic and volunteer info too
function Dataview(args){

    return(
    <Paper elevation={3}>
       <ContactInfo name="mike" address="123" phone="717" email="a@a.com" summary="ss"/> 
       <Donations />
    </Paper>
    
    );
}


export default Dataview;