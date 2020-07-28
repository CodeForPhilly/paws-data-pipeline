import React, {useState} from 'react';
import {Container, MenuItem, Select, FormControl, InputLabel, Button} from "@material-ui/core";

import useFetch from './scripts/useFetch';

// These "forms" can be refactored to be a resuable component
// https://reactjs.org/docs/forms.html

function DownloadForm(props) {
  const [downloadSource, setDownloadSource] = useState("current");

  const makePath = (value) => {
    return `http://localhost:3333/files/${value}?download_${value}_btn=${value}+sources`
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
  const [{response, isLoading, isError}, setUrl] = useFetch(null, null);

  const execute = (event)=>{
    event.preventDefault();

    fetch("/execute")
      .then(response => response.json())
      .then(data => console.log(data))
      .catch(error => console.log(error));
  };

  return (
    <div>
    <form onSubmit={props.handleSubmit}>
        <input type="file" ref={props.fileInput} multiple />
        <button type="submit">Submit</button>
    </form>
    </div>
  );

}
export { UploadForm, DownloadForm };