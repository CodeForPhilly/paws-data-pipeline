import React from 'react';
import Button from '@material-ui/core/Button';
import Dialog from '@material-ui/core/Dialog';
import DialogActions from '@material-ui/core/DialogActions';
import DialogContent from '@material-ui/core/DialogContent';
import DialogContentText from '@material-ui/core/DialogContentText';
import DialogTitle from '@material-ui/core/DialogTitle';

import useToken from './Login/useToken';

import Refresh from './Refresh';

export default function  RefreshDlg(props) {
  const [open, setOpen] = React.useState(props.shouldOpen);
  const { access_token } = useToken();  // We want to use the passed-in top-level setToken

  const handleClose = async (shouldRefresh) => {
    // Could be closed with Yes, No, outclick (which equals No)
    setOpen(false);
    if (props.shouldOpen){
      const new_at =  await Refresh(access_token);
      props.setToken(new_at);
    }
  };



  return (
    <div>
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
