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
import { withStyles } from '@material-ui/core/styles';
import moment from 'moment';
import EmojiPeopleIcon from '@material-ui/icons/EmojiPeople';
import DataTableHeader from './DataTableHeader';

const customStyles = theme => ({
    spaceIcon: {
        marginTop: 3,
        marginRight: 3
    },
    headerCell: {
        fontWeight: "bold"
    },
});

class volunteerActivity extends Component {

    render() {
        const {classes, volunteer} = this.props;
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
                                    <TableCell className={classes.headerCell}>Volunteer activity start</TableCell>
                                    <TableCell className={classes.headerCell}>Life hours</TableCell>
                                    <TableCell className={classes.headerCell}>YTD hours</TableCell>
                                </TableRow>
                            </TableHead>
                            <TableBody>
                                { this.props.volunteer && (
                                <TableRow>
                                    <TableCell>{
                                        (volunteer.start_date === "N/A") 
                                        ? "N/A" 
                                        : moment(volunteer.start_date).format("MM-DD-YYYY")
                                    }
                                    </TableCell>
                                    <TableCell>{volunteer.life_hours.toFixed(2)}</TableCell>
                                    <TableCell>{volunteer.ytd_hours.toFixed(2)}</TableCell>
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


export default withStyles(customStyles)(volunteerActivity);