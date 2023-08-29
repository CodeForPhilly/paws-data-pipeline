import React from "react";
import {
    Grid,
    TableRow,
    TableContainer,
    TableCell,
    TableBody,
    Table,
    Divider,
} from "@material-ui/core";
import _ from "lodash";
import { formatTimestamp, formatUploadType } from "../../../utils/utils";

export default function UploadsTable(props) {
    const { tableData } = props;

    return (
        <Grid item>
            <Divider />
            <Grid item>
                <TableContainer>
                    <Table aria-label="simple table">
                        <TableBody>
                            <TableRow key="upload-header">
                                <TableCell
                                    align="left"
                                    component="th"
                                    scope="row"
                                >
                                    <b>Upload Type</b>
                                </TableCell>
                                <TableCell>
                                    <b>Last Execution</b>
                                </TableCell>
                            </TableRow>
                            {_.map(tableData, (row, index) => (
                                <TableRow key={`last_run_${index}`}>
                                    <TableCell
                                        align="left"
                                        component="th"
                                        scope="row"
                                    >
                                        {formatUploadType(Object.keys(row)[0])}
                                    </TableCell>
                                    <TableCell
                                        align="left"
                                        component="th"
                                        scope="row"
                                    >
                                        {formatTimestamp(Object.values(row)[0])}
                                    </TableCell>
                                </TableRow>
                            ))}
                        </TableBody>
                    </Table>
                </TableContainer>
            </Grid>
        </Grid>
    );
}
