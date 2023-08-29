import React from "react";
import {
    Button,
    Grid,
    Paper,
    Typography,
    CardContent,
} from "@material-ui/core";
import _ from "lodash";
import AnalysisTable from "./AnalysisTable";

export default function AnalysisBox(props) {
    const { handleExecute, lastExecution, statistics } = props;

    return (
        <Grid container item direction="column" spacing={3} sm={6}>
            <Grid item>
                <Paper>
                    <CardContent>
                        <Typography variant="h5" style={{ paddingBottom: 5 }}>
                            Run New Analysis
                        </Typography>
                        <form onSubmit={handleExecute}>
                            <Button
                                type="submit"
                                variant="contained"
                                color="primary"
                            >
                                Run Data Analysis
                            </Button>
                        </form>
                    </CardContent>
                    {!_.isEmpty(statistics) && (
                        <AnalysisTable
                            lastExecution={lastExecution}
                            tableData={statistics}
                        />
                    )}
                </Paper>
            </Grid>
        </Grid>
    );
}
