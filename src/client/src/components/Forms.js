import React, {useState, useEffect} from 'react';
import {Input, MenuItem, Select, FormControl, InputLabel} from "@material-ui/core";

/* These "forms" can be refactored to be a resuable component */
function DownloadForm(props) {

  return (
    <FormControl>
      <InputLabel id="download-source-select-label">Select Download Source</InputLabel>
      <Select labelId="download-source-select-label">
        <MenuItem>Current Items</MenuItem>
        <MenuItem>Archived</MenuItem>
        <MenuItem>Other</MenuItem>
      </Select>
      <Input inputComponent="input" type="file" />
    </FormControl>
  );

}

function UploadForm(props) {

  const [files, setFiles] = useState(null);

  const request = new Request('/file/upload', {
      method: 'POST',
      body:  FileList,
      header: new Headers({'Content-Type':'multipart/form-data'})
  });

  return (
    <FormControl>
      <InputLabel id="upload-source-select-label">Select Input Source</InputLabel>
      <Select labelId="upload-source-select-label">
        <MenuItem>Salesforce</MenuItem>
        <MenuItem>Volgistics</MenuItem>
        <MenuItem>Petpoint</MenuItem>
      </Select>
      <Input inputComponent="input" type="file" />
    </FormControl>
  );

}
export { UploadForm, DownloadForm };