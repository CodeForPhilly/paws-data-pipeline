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
import { formatTimestamp } from "../../../utils/utils";

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
                                {formatTimestamp(lastExecution)}
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
