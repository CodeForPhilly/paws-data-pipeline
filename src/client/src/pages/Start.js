import React from "react";
import { makeStyles, Paper} from '@material-ui/core';

const useStyles = makeStyles({
    content:{
      minHeight: '95vh'
    },
    paper:{
      minHeight: '95vh',
      backgroundImage: '../../../public/background.jpg'
    }

});

function StartPage(props) {
  const classes = useStyles();
  return <Paper elevation={3} classes={classes.paper} />
}

export default StartPage;