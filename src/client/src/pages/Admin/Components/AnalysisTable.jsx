import React from "react";
import {
    Grid,
    TableRow,
    TableCell,
    TableBody,
    Table,
    Divider,
} from "@material-ui/core";
import moment from "moment-timezone";
import _ from "lodash";

export default function AnalysisTable(props) {
    const { tableData, lastExecution } = props;

    return (
        <Grid item>
            <Divider />
            <Table aria-label="simple table">
                <TableBody>
                    <TableRow key="time">
                        <TableCell align="left" component="th" scope="row">
                            <b>Last Analysis</b>
                        </TableCell>
                        <TableCell align="left">
                            <b>
                                {moment(
                                    lastExecution,
                                    "dddd MMMM Do h:mm:ss YYYY"
                                )
                                    .local()
                                    .format("MMMM Do YYYY, h:mm:ss a")}
                            </b>
                        </TableCell>
                    </TableRow>
                    {tableData.map((row, index) => (
                        <TableRow key={index}>
                            <TableCell align="left" component="th" scope="row">
                                {row[0]}
                            </TableCell>
                            <TableCell align="left">{row[1]}</TableCell>
                        </TableRow>
                    ))}
                </TableBody>
            </Table>
        </Grid>
    );
}
