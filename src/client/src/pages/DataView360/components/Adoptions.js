import React, { Component } from 'react';
import { Paper, Typography, Table, TableContainer, TableHead, TableBody, TableRow, TableCell, Container} from '@material-ui/core';
import { withStyles } from '@material-ui/core/styles';
import "./styles/Adoptions.css";
import _ from 'lodash';
import moment from 'moment';

const ROWS_TO_SHOW = 3

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

class Adoptions extends Component {
    constructor(props) {
        super(props);

        this.createRows = this.createRows.bind(this);
    }

    createRows(adoptions){
        adoptions = _.map(adoptions, pet => {
            return pet.json;
        });
        const adoptionsSorted = _.sortBy(adoptions, 'outcome_date');
        const latestAdoptions = adoptionsSorted.slice(0,ROWS_TO_SHOW);

        const result = _.map(latestAdoptions, pet => {
            return(<StyledTableRow>
                    <TableCell align="center">{moment(pet.outcome_date).format("YYYY-MM-DD")}</TableCell>
                    <TableCell align="center">{pet.animal_name}</TableCell>
                    <TableCell align="center">{pet.animal_type}</TableCell>
                    <TableCell align="center">{pet.primary_breed}</TableCell>
                    <TableCell align="center">{pet.animal_num}</TableCell>
                    <TableCell align="center">{pet.age_group}</TableCell>
                </StyledTableRow>);

            });

        return result;
    }

    render() {
        return (<Container style={{"marginTop":"1em"}}>
                    <Typography align='center' gutterBottom='true' variant='h4'>Adoption/Foster Records(Top 3)</Typography>
                    <TableContainer style={{"marginTop":"1em"}} component={Paper} variant='outlined'>
                        <Table>
                            <TableHead>
                                <TableRow>
                                    <StyledTableCell align="center">Date of Adoption</StyledTableCell>
                                    <StyledTableCell align="center">Name</StyledTableCell>
                                    <StyledTableCell align="center">Type/Species</StyledTableCell>
                                    <StyledTableCell align="center">Primary Breed</StyledTableCell>
                                    <StyledTableCell align="center">Animal-Number</StyledTableCell>
                                    <StyledTableCell align="center">Current Age</StyledTableCell>
                                </TableRow>
                            </TableHead>
                            <TableBody>
                                { this.props.adoptions && this.createRows(this.props.adoptions) }
                            </TableBody>
                        </Table>
                   </TableContainer>
                </Container>
        );
    }
}


export default Adoptions;