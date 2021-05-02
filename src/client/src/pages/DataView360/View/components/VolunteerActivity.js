import React, { Component } from 'react';
import {
    Paper,
    Typography,
    Table,
    TableContainer,
    TableHead,
    TableBody,
    TableRow,
    TableCell,
    Container,
} from '@material-ui/core';
import { withStyles } from '@material-ui/core/styles';
import _ from 'lodash';
import moment from 'moment';
import Grid from "@material-ui/core/Grid";
import EmojiPeopleIcon from '@material-ui/icons/EmojiPeople';
import TimelineIcon from '@material-ui/icons/Timeline';
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
        const {classes} = this.props;

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
                                    <TableCell>{moment(this.props.volunteer.start_date).format("MM-DD-YYYY")}</TableCell>
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


export default withStyles(customStyles)(volunteerActivity);