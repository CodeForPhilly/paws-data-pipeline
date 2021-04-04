import React, {Component} from 'react';
import {
    Paper,
    Typography,
    Table,
    TableContainer,
    TableHead,
    TableBody,
    TableRow,
    TableCell,
    Container
} from '@material-ui/core';
import {withStyles} from '@material-ui/core/styles';
import styles from "./styles/Adoptions.module.css";
import "./styles/table.css";
import _ from 'lodash';
import moment from "moment";


const StyledTableCell = withStyles((theme) => ({
    head: {
        backgroundColor: 'initial', // here
        fontWeight: 600,
    }
}))(TableCell);

const StyledTableRow = withStyles((theme) => ({
    root: {
        '&:nth-of-type(even)': {
            backgroundColor: 'initial', // and here
        }
    }
}))(TableRow);

const PET_COUNT = 3;

class Adoptions extends Component {

    getLatestPets(petList) {
        let retVal;

        if (petList) {
            retVal = petList.slice(0, PET_COUNT);
        }

        return retVal;
    }

    getAnimalAge(epochTime) {
        let dateOfBirth = moment(epochTime * 1000);
        return moment().diff(dateOfBirth, 'years');
    }

    render() {
        // todo: update when we add pet info
        // todo: clean array of animal_id
        const numOfPets = _.size(this.props.adoptions);
        const latestPets = this.getLatestPets(this.props.adoptions);

        return (<Container className={styles.adoptions} style={{"marginTop": "1em"}}>
                <Typography className={styles.adoptions_title} variant='h4'>Adoption/Foster
                    Records {(numOfPets > 3) && "(Showing 3 Pets out of " + numOfPets + ")"}</Typography>
                <TableContainer className="main_table_container" style={{"marginTop": "1em"}} component={Paper}
                                variant='outlined'>
                    <Table className="main_table">
                        <TableHead>
                            <TableRow>
                                <StyledTableCell align="center">Name</StyledTableCell>
                                <StyledTableCell align="center">Animal Type</StyledTableCell>
                                <StyledTableCell align="center">Breed</StyledTableCell>
                                <StyledTableCell align="center">Age</StyledTableCell>
                                <StyledTableCell align="center">Photo</StyledTableCell>
                            </TableRow>
                        </TableHead>
                        <TableBody>
                            {_.map(latestPets, (adoptionInfo, index) => {

                                const photoLink = _.get(adoptionInfo, "Photos.[0]");
                                const photo = <img src={photoLink} alt="animal" style={{"maxWidth": "100px"}}/>

                                return <StyledTableRow key={index}>
                                    <TableCell align="center">{adoptionInfo["Name"]}</TableCell>
                                    <TableCell align="center">{adoptionInfo["Type"]}</TableCell>
                                    <TableCell align="center">{adoptionInfo["Breed"]}</TableCell>
                                    <TableCell
                                        align="center">{this.getAnimalAge(adoptionInfo["DOBUnixTime"])}</TableCell>
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