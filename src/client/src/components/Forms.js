import React, {useState, useEffect} from 'react';
import {Input, MenuItem, Select, FormControl, InputLabel, Button} from "@material-ui/core";

import useFetch from './scripts/useFetch';

// These "forms" can be refactored to be a resuable component
// https://reactjs.org/docs/forms.html

function DownloadForm(props) {

  const handleChange = (event)=>{
    event.preventDefault();

    fetch("/files/current")
      .then(response => response.formData())
      .then(files => console.log(files));
  }

  return (
    <form onSubmit={handleChange}>
    <FormControl>
>
      <button type="submit">Download</button>
    </FormControl>
    </form>
  );

}

// Still need to refresh the list of availabe files on Server.
// <Input /> objects are uncontrolled in React, so it is recommend that you use
// the File API to interact with selected files. 
// https://reactjs.org/docs/uncontrolled-components.html#the-file-input-tag

function UploadForm(props) {
  const fileInput = React.createRef();
  const [{response, isLoading, isError}, setUrl] = useFetch(null, null);

  const handleSubmit = (event)=>{
    //Prevent default reload on submit
    event.preventDefault();

    // Use FormData element for each file in fileInput
    var formData = new FormData();
    Array.from(fileInput.current.files).forEach(element => {
      formData.append('file', element, element.name)
    });

    fetch("/file", { method:'POST', body:formData })
      .then(resp => resp.text())
      .then(resp => console.log(resp))
      .catch(error => console.log(error));
  }

  return (
    <form onSubmit={handleSubmit}>
        <input type="file" ref={fileInput} multiple />
        <button type="submit">Submit</button>
    </form>
  );

}
export { UploadForm, DownloadForm };