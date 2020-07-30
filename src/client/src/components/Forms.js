import React, {useState} from 'react';
import {Container, MenuItem, Select, FormControl, InputLabel, Button} from "@material-ui/core";

import useFetch from './scripts/useFetch';

// These "forms" can be refactored to be a resuable component
// https://reactjs.org/docs/forms.html

function DownloadForm(props) {
  const [downloadSource, setDownloadSource] = useState("current");

  const makePath = (value) => {
    return `http://localhost:3000/api/files/${value}?download_${value}_btn=${value}+sources`
  }

  const handleChange = (event)=>{
    setDownloadSource(event.target.value)
  }

  return (
    <Container>
    <FormControl>
      <Select value={downloadSource}
              onChange={handleChange}>
        <InputLabel>Select Item to Download</InputLabel>
        <MenuItem value={'current'}>Current</MenuItem>
        <MenuItem value={'archived'}>Archived</MenuItem>
        <MenuItem value={'output'}>Output</MenuItem>
      </Select>
    </FormControl>
    <Button href={makePath(downloadSource)}>Download</Button>
    </Container>
  );

}

// Still need to refresh the list of availabe files on Server.
// <Input /> objects are uncontrolled in React, so it is recommend that you use
// the File API to interact with selected files. 
// https://reactjs.org/docs/uncontrolled-components.html#the-file-input-tag

function UploadForm(props) {
  return (
    <div>
        <form onSubmit={props.handleUpload}>
            <input type="file" ref={props.fileInput} multiple />
            <button type="submit">Upload</button>
        </form>
    </div>
  );
}

function ExecuteForm(props) {
    return (
        <div>
            <form onSubmit={props.handleExecute}>
                <button type="submit">Execute</button>
            </form>
        </div>
    );
}

export { UploadForm, DownloadForm, ExecuteForm };