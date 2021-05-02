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
import { makeStyles, withStyles } from '@material-ui/core/styles';
import _ from 'lodash';
import moment from 'moment';
import Grid from "@material-ui/core/Grid";
import EmojiPeopleIcon from '@material-ui/icons/EmojiPeople';
import TimelineIcon from '@material-ui/icons/Timeline';


const customStyles = makeStyles({
    spaceIcon: {
        marginTop: 3,
        marginRight: 3
    },
    headerCell: {
        fontWeight: "bold"
    },
});

function DataTableHeader(props) {
    const classes = customStyles();
    const { headerText, emojiIcon } = props;
    return (
        <Typography variant='h5'>
            <Grid container style={{ "margin": "0.5em" }} direction={'row'}>
                <Grid item className={classes.spaceIcon}>
                    { emojiIcon }
                </Grid>
                <Grid item>
                    { headerText }
                </Grid>
            </Grid>
        </Typography>
    );
}

export default withStyles(customStyles)(DataTableHeader);