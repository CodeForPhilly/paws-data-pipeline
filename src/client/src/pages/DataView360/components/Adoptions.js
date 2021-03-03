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
        const numAdoptions = _.size(this.props.adoptions);
        return (<Container className={styles.adoptions} style={{"marginTop":"1em"}}>
                    <Typography className={styles.adoptions_title} variant='h4'>Adoption/Foster Records {(numAdoptions > 3) && "(Showing latest 3 out of " + numAdoptions + ")"}</Typography>
                    <TableContainer className="main_table_container" style={{"marginTop":"1em"}} component={Paper} variant='outlined'>
                        <Table className="main_table">
                            <TableHead>
                                <TableRow>
                                    <StyledTableCell align="center">Name</StyledTableCell>
                                    <StyledTableCell align="center">Adoption Type</StyledTableCell>
                                    <StyledTableCell align="center">Adoption Subtype</StyledTableCell>
                                    <StyledTableCell align="center">Animal Type</StyledTableCell>
                                    <StyledTableCell align="center">Breed</StyledTableCell>
                                    <StyledTableCell align="center">Age</StyledTableCell>
                                    <StyledTableCell align="center">Photo</StyledTableCell>
                                </TableRow>
                            </TableHead>
                            <TableBody>
                                {_.map(this.props.adoptions, (adoptionInfo, index) => {
                                    const photoLink = adoptionInfo["animal_details"]["Photos"][0]
                                    const photo = <img src={photoLink} style={{"maxWidth": "100px"}}/>;
                                    return <StyledTableRow key={adoptionInfo["Time"] + index}>
                                    <TableCell align="center">{adoptionInfo["animal_details"]["Name"]}</TableCell>
                                    <TableCell align="center">{adoptionInfo["Type"]}</TableCell>
                                    <TableCell align="center">{adoptionInfo["Subtype"]}</TableCell>
                                    <TableCell align="center">{adoptionInfo["animal_details"]["Type"]}</TableCell>
                                    <TableCell align="center">{adoptionInfo["animal_details"]["Breed"]}</TableCell>
                                    <TableCell align="center">{(parseInt(adoptionInfo["animal_details"]["Age"])/12).toFixed(2)}</TableCell>
                                    <TableCell align="center">{photo}</TableCell>
                                </StyledTableRow>
                                })}
                            </TableBody>
                        </Table>
                   </TableContainer>
                </Container>
        );
    }
}


export default Adoptions;