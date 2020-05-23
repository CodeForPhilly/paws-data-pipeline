import  React, { useState, useEffect } from "react";
import {Tabs, Tab, Container, Paper } from "@material-ui/core";
import Skeleton from "@material-ui/lab/Skeleton";
import { makeStyles } from "@material-ui/core/styles";

import TabPanel from '../components/TabPanel';
import { UploadForm, DownloadForm } from '../components/Forms';
import useFetch from "../components/scripts/useFetch";

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

    const handleChange = (event, newIndex) => {
        setActiveIndex(newIndex);
        setUrl("/listCurrentFiles");
    };

    const [{data, isLoading, isError}, setUrl] = useFetch("/listCurrentFiles", null);

  const files = data ? 
      <div><ul>{data.map((i)=><li>{i}</li>)}</ul></div> :
      <Skeleton variant="rect" width={400} height={400}>No Files Found</Skeleton> ;

    return (
      <Container classes={classes.content}>
        <Tabs value={activeIndex} onChange={handleChange} aria-label="upload-download-reports-tabs">
          <Tab label="Upload" />
          <Tab label="Download" />
          <Tab label="Reports" />
        </Tabs>
        <TabPanel value={activeIndex} index={0}> 
          {files} 
          <UploadForm />
        </TabPanel>
        <TabPanel value={activeIndex} index={1}>
          {files}
          <DownloadForm />
        </TabPanel>
        <TabPanel value={activeIndex} index={2}>
          <Skeleton variant="rect" width={400} height={400}>Select File to Load</Skeleton>
        </TabPanel>
      </Container>
    );
}

export default Content;
