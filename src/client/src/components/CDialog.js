import React from 'react';
import Button from '@material-ui/core/Button';
import Dialog from '@material-ui/core/Dialog';
import DialogActions from '@material-ui/core/DialogActions';
import DialogContent from '@material-ui/core/DialogContent';
import DialogContentText from '@material-ui/core/DialogContentText';
import DialogTitle from '@material-ui/core/DialogTitle';

import useToken from '../components/Login/useToken';

import Refresh from './Refresh';

export default function  CDialog() {
  const [open, setOpen] = React.useState(true);
  const { access_token, setToken } = useToken();


  const handleClickOpen = () => {
    setOpen(true);
  };

  const handleClose = async (shouldRefresh) => {
    setOpen(false);
    console.log("Refresh? " + String(shouldRefresh));
    if (shouldRefresh){
      const new_at =  await Refresh(access_token);
      setToken(new_at);
    }
  };



  return (
    <div>
      {/* <Button variant="outlined" color="primary" onClick={handleClickOpen}>
        Open alert dialog
      </Button> */}
      <Dialog
        open={open}
        onClose={() => handleClose(false)}
        aria-labelledby="alert-dialog-title"
        aria-describedby="alert-dialog-description"
      >
        <DialogTitle id="alert-dialog-title">{"You are about to be logged out!"}</DialogTitle>
        <DialogContent>
          <DialogContentText id="alert-dialog-description">
            Stay logged in to keep working?
          </DialogContentText>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => handleClose(false)} color="primary">
            No
          </Button>
          <Button onClick={() => handleClose(true)} color="primary" autoFocus>
           Yes
          </Button>
        </DialogActions>
      </Dialog>
    </div>
  );
}
