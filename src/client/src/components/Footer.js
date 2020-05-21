import  React from "react";
import {Box, Toolbar } from "@material-ui/core";

import useFetch from "./scripts/useFetch";

export default function Footer(props){
  const [{data, isLoading, isError},setUrl] = useFetch('/time', "0"); 

  return (
      <Box id="footer">
        <Toolbar>
            <h2>The time is: {data.time}</h2>
        </Toolbar>
      </Box>
  );

}
