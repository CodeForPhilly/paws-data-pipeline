import  React, { useState, useEffect } from "react";
import {Tabs, Tab, Container, Paper } from "@material-ui/core";
import Skeleton from "@material-ui/lab/Skeleton";
import { makeStyles } from "@material-ui/core/styles";

import TabPanel from '../components/TabPanel';
import { UploadForm, DownloadForm, ExecuteForm } from '../components/Forms';

const useStyles = makeStyles({
    content:{
      minHeight: '95vh'
    },
    paper:{
      minHeight: '95vh',
    }

});

function Content(props){
    const [activeIndex, setActiveIndex] = React.useState(0);
    const classes = useStyles();
    const fileInput = React.createRef();
    const [data, setData] = useState(null);
    const [reload, setReload] = useState(false);

    const handleChange = (event, newIndex) => {
        setActiveIndex(newIndex);
    };

    //const [{data, isLoading, isError}, setUrl] = useFetch("/listCurrentFiles", null);

    const handleUpload = (event)=>{
      //Prevent default reload on submit
      event.preventDefault();

      // Use FormData element for each file in fileInput
      var formData = new FormData();
      Array.from(fileInput.current.files).forEach(element => {
        formData.append('file', element, element.name)
      })

      fetch("/api/file", { method:'POST', body:formData })
        .then(response => response.text())
        .then(text=>console.log(text))
        .catch(error => console.log(error));

      console.log(reload);
      setReload(!reload);
      console.log(reload);
    };

    const handleExecute = useEffect(()=>{
        fetch('/api/execute')
            .then(response => response.json())
            .catch(error => console.log(error))
    });
    // May need to submit twice to refresh,
    // need to figure out why?
    useEffect(()=>{
      fetch("/api/listCurrentFiles")
        .then(response=>response.json())
        .then(data => setData(data))
        .catch(error=>console.log(error));
    },[reload]);

    const files = data ? 
      <div><ul>{data.map((i)=><li>{i}</li>)}</ul></div> :
      <Skeleton variant="rect" width={400} height={400}>No Files Found</Skeleton> ;


    return (
      <Container classes={classes.content}>
        <Paper elevation={2} style={{"marginTop":"1em", "padding":"2em"}}>
        <Tabs value={activeIndex} onChange={handleChange} aria-label="upload-download-reports-tabs">
          <Tab label="Upload" />
          <Tab label="Download" />
          <Tab label="Execute" />
        </Tabs>

        <TabPanel value={activeIndex} index={0}> 
          {files}
          <UploadForm fileInput={fileInput} handleUpload={handleUpload}/>
        </TabPanel>
        <TabPanel value={activeIndex} index={1}>
          {files}
          <DownloadForm />
        </TabPanel>
        <TabPanel value={activeIndex} index={2}>
          <ExecuteForm handleExecute={handleExecute}/>
        </TabPanel>
        </Paper>
      </Container>
    );
}

export default Content;
