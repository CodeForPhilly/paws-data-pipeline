import React, {useState} from 'react';
import {MenuItem, Select, FormControl, InputLabel, Button} from "@material-ui/core";
import Grid from '@material-ui/core/Grid';

import CardContent from '@material-ui/core/CardContent';


function DownloadForm(props) {
  const [downloadSource, setDownloadSource] = useState("current");

  const makePath = (value) => {
    return `http://localhost:3000/api/files/${value}?download_${value}_btn=${value}+sources`
  }

  const handleChange = (event)=>{
    setDownloadSource(event.target.value)
  }

  return (
    <div>
        <CardContent>
            <Grid container spacing={3}>
                <Grid item>
                    <FormControl>
                          <Select value={downloadSource} onChange={handleChange} style={{"minWidth": "30px"}}>
                            <InputLabel style={{"padding": "10px"}}>Select Item to Download</InputLabel>
                            <MenuItem value={'current'}>Current</MenuItem>
                            <MenuItem value={'archived'}>Archived</MenuItem>
                            <MenuItem value={'output'}>Output</MenuItem>
                          </Select>
                    </FormControl>
                </Grid>
                <Grid item>
                    <Button href={makePath(downloadSource)} variant="contained" color="primary">Download</Button>
                </Grid>
            </Grid>
        </CardContent>
    </div>
  );

}

function UploadForm(props) {
  return (
    <div>
        <form onSubmit={props.handleUpload}>
            <CardContent>
                <input type="file" value={props.fileInput} multiple />
                <Button type="submit" variant="contained" color="primary">Upload</Button>
            </CardContent>
        </form>
    </div>
  );
}

function ExecuteForm(props) {
    return (
        <div>
            <form onSubmit={props.handleExecute}>
                <CardContent>
                    <Button type="submit" variant="contained" color="primary">Execute</Button>
                </CardContent>
            </form>
        </div>
    );
}

export { UploadForm, DownloadForm, ExecuteForm };