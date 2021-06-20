import React, { Component } from 'react';
import {
    Paper,
    Table,
    TableContainer,
    TableHead,
    TableBody,
    TableRow,
    TableCell,
    Container,
} from '@material-ui/core';
import moment from 'moment';
import EmojiPeopleIcon from '@material-ui/icons/EmojiPeople';
import DataTableHeader from './DataTableHeader';


class VolunteerActivity extends Component {

    render() {
        return (
            <React.Fragment>
                <Container component={Paper} style={{"marginTop": "1em"}}>
                    <DataTableHeader headerText={"Volunteer Activity"} 
                        emojiIcon={<EmojiPeopleIcon color='primary' fontSize='inherit'/>}
                    />
                    <TableContainer component={Paper} style={{"marginBottom": "1em"}} variant='outlined'>
                        <Table>
                            <TableHead>
                                <TableRow>
                                    <TableCell>Volunteer activity start</TableCell>
                                    <TableCell>Life hours</TableCell>
                                    <TableCell>YTD hours</TableCell>
                                </TableRow>
                            </TableHead>
                            <TableBody>
                                { this.props.volunteer && (
                                <TableRow>
                                    <TableCell>{
                                        (this.props.volunteer.start_date === "N/A")
                                        ? "N/A" 
                                        : moment(this.props.volunteer.start_date).format("YYYY-MM-DD")
                                    }
                                    </TableCell>
                                    <TableCell>{this.props.volunteer.life_hours.toFixed(2)}</TableCell>
                                    <TableCell>{this.props.volunteer.ytd_hours.toFixed(2)}</TableCell>
                                </TableRow>
                                )}
                            </TableBody>
                        </Table>
                    </TableContainer>
                </Container>
            </React.Fragment>
        );
    }
}


export default VolunteerActivity;