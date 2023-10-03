import React from "react";
import {
    Button,
    Grid,
    Paper,
    Typography,
    CardContent,
} from "@material-ui/core";
import _ from "lodash";
import UploadsTable from "./UploadsTable";

export default function UploadBox(props) {
    const { filesInput, handleUpload, lastUploads } = props;

    return (
        <Grid item direction="column" spacing={3} sm={6}>
            <Paper>
                <CardContent>
                    <Typography variant="h5">Upload Files</Typography>
                    <Typography variant="caption">Note: This upload feature now only accepts Volgistics data files. Other data is uploaded automatically.</Typography>
                    <form onSubmit={handleUpload}>
                        <input type="file" id="fileItemsID"
                            value={filesInput}
                            multiple
                        />
                        <Button 
                            type="submit" 
                            variant="contained" 
                            color="primary"
                        >
                            Upload
                        </Button>
                    </form>
                </CardContent>
                {!_.isEmpty(lastUploads) &&
                    <UploadsTable tableData={lastUploads} />
                }
            </Paper>
        </Grid>
    );
}
