import  React, { useState, useEffect } from "react";
import {Tabs, Tab, Container } from "@material-ui/core";
import Skeleton from "@material-ui/lab/Skeleton";
import { makeStyles } from "@material-ui/core/styles";

import TabPanel from '../components/TabPanel';
import { UploadForm, DownloadForm } from '../components/Forms';

const useStyles = makeStyles({
    content:{
      minHeight: '95vh'
    },
    paper:{
      minHeight: '95vh',
      backgroundImage: '../../../public/background.jpg'
    }

});

function Content(props){
    const [activeIndex, setActiveIndex] = React.useState(0);
    const classes = useStyles();

    const handleChange = (event, newIndex) => {
        setActiveIndex(newIndex)
    };

    return (
      <Container classes={classes.content}>
        <Tabs value={activeIndex} onChange={handleChange} aria-label="upload-download-reports-tabs">
          <Tab label="Upload" />
          <Tab label="Download" />
          <Tab label="Reports" />
        </Tabs>
        <TabPanel value={activeIndex} index={0}> 
          <Skeleton variant="rect" width={400} height={400}> Select File to Load</Skeleton>
          <UploadForm />
        </TabPanel>
        <TabPanel value={activeIndex} index={1}>
          <Skeleton variant="rect" width={400} height={400}>Select File to Load</Skeleton>
          <DownloadForm />
        </TabPanel>
        <TabPanel value={activeIndex} index={2}>
          <Skeleton variant="rect" width={400} height={400}>Select File to Load</Skeleton>
        </TabPanel>
      </Container>
    );
}

export default Content;
