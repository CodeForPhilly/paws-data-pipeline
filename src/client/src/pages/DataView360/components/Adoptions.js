import React, { Component } from 'react';
import { Paper, Typography, Table, TableContainer, TableHead, TableBody, TableRow, TableCell, Container} from '@material-ui/core';
import { withStyles } from '@material-ui/core/styles';
import styles from "./styles/Adoptions.module.css";
import "./styles/table.css";
import _ from 'lodash';
import moment from 'moment';

const ROWS_TO_SHOW = 3

/* I don't khow, how to remove it. So I changed background-color on 'initial' */
const StyledTableCell = withStyles((theme)=>({
    head:{
        backgroundColor: 'initial', // here
        fontWeight: 600,
    }
}))(TableCell);

const StyledTableRow = withStyles((theme)=>({
    root:{
        '&:nth-of-type(even)':{
            backgroundColor: 'initial', // and here
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
                    <TableCell>{moment(pet.outcome_date).format("YYYY-MM-DD")}</TableCell>
                    <TableCell>{pet.animal_name}</TableCell>
                    <TableCell>{pet.animal_type}</TableCell>
                    <TableCell>{pet.primary_breed}</TableCell>
                    <TableCell>{pet.animal_num}</TableCell>
                    <TableCell>{pet.age_group}</TableCell>
                </StyledTableRow>);

            });

        return result;
    }

    render() {
        return (<Container className={styles.adoptions}>
                    <Typography className={styles.adoptions_title} gutterBottom='true' variant='h4'>Adoption/Foster Records(Top 3)</Typography>
                    <TableContainer className="main_table_container" style={{"marginTop":"1em"}} component={Paper} variant='outlined'>
                        <Table className="main_table">
                            <TableHead>
                                <TableRow>
                                    <StyledTableCell>Date of Adoption</StyledTableCell>
                                    <StyledTableCell>Name</StyledTableCell>
                                    <StyledTableCell>Type/Species</StyledTableCell>
                                    <StyledTableCell>Primary Breed</StyledTableCell>
                                    <StyledTableCell>Animal-Number</StyledTableCell>
                                    <StyledTableCell>Current Age</StyledTableCell>
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