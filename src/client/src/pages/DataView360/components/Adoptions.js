import React, { Component } from 'react';
import { Paper, Typography, Table, TableContainer, TableHead, TableBody, TableRow, TableCell, Container} from '@material-ui/core';
import { withStyles } from '@material-ui/core/styles';
import "./styles/Adoptions.css";
import _ from 'lodash';

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
    }

    getAnimalIds() {
        let result = [];

        let animal_ids = _.get(this.props, 'adoptions[0].animal_ids');
        if(animal_ids) {
            result = _.filter(animal_ids.split("'"), item => {
                return _.isNaN(_.parseInt(item)) !== true;
            })
        }
    }

    render() {
        // todo: update when we add pet info
        // todo: clean array of animal_id
        return (<Container style={{"marginTop":"1em"}}>
                    <Typography align='center' gutterBottom='true' variant='h4'>Adoption/Foster Records(Top 3)</Typography>
                    <TableContainer style={{"marginTop":"1em"}} component={Paper} variant='outlined'>
                        <Table>
                            <TableHead>
                                <TableRow>
                                    <StyledTableCell align="center">Number of Adoptions</StyledTableCell>
                                </TableRow>
                            </TableHead>
                            <TableBody>
                                <StyledTableRow>
                                    <TableCell align="center"> {_.size(this.getAnimalIds())}</TableCell>
                                </StyledTableRow>
                            </TableBody>
                        </Table>
                   </TableContainer>
                </Container>
        );
    }
}


export default Adoptions;