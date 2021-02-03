import React, { Component } from 'react';
import { Paper, Typography, Table, TableContainer, TableHead, TableBody, TableRow, TableCell, Container} from '@material-ui/core';
import { withStyles } from '@material-ui/core/styles';
import styles from "./styles/Adoptions.module.css";
import "./styles/table.css";
import _ from 'lodash';

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

    getAnimalIds() {
        let result = [];

        let animal_ids = _.get(this.props, 'adoptions[0].animal_ids');
        if(animal_ids) {
            result = _.filter(animal_ids.split("'"), item => {
                return _.isNaN(_.parseInt(item)) !== true;
            })
        }

        return result;
    }

    render() {
        // todo: update when we add pet info
        // todo: clean array of animal_id
        return (<Container className={styles.adoptions} style={{"marginTop":"1em"}}>
                    <Typography className={styles.adoptions_title} variant='h4'>Adoption/Foster Records (Top 3)</Typography>
                    <TableContainer className="main_table_container" style={{"marginTop":"1em"}} component={Paper} variant='outlined'>
                        <Table className="main_table">
                            <TableHead>
                                <TableRow>
                                    <StyledTableCell align="center">Number of Adoptions</StyledTableCell>
                                </TableRow>
                            </TableHead>
                            <TableBody>
                                <StyledTableRow>
                                    <TableCell align="center"> {_.size(this.props.adoptions)}</TableCell>
                                </StyledTableRow>
                            </TableBody>
                        </Table>
                   </TableContainer>
                </Container>
        );
    }
}


export default Adoptions;