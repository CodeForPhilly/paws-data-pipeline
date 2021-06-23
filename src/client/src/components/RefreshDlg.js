import React from 'react';
import Button from '@material-ui/core/Button';
import Dialog from '@material-ui/core/Dialog';
import DialogActions from '@material-ui/core/DialogActions';
import DialogContent from '@material-ui/core/DialogContent';
import DialogContentText from '@material-ui/core/DialogContentText';
import DialogTitle from '@material-ui/core/DialogTitle';

import useToken from '../pages/Login/useToken';

import Refresh from './Refresh';
import defaultTheme from "../theme/defaultTheme";


export default function RefreshDlg(props) {
    const [open, setOpen] = React.useState(props.shouldOpen);
    const {access_token} = useToken();  // We want to use the passed-in top-level setToken

    const handleClose = async (shouldRefresh) => {
        // Could be closed with Yes, No, outclick (which equals No)
        setOpen(false);
        if (shouldRefresh) {
            const new_at = await Refresh(access_token);
            props.setToken(new_at);
        }
    };


    return (
        <div>
            <Dialog
                PaperProps={{
                    style: {
                        zIndex: defaultTheme.zIndex.drawer + 2
                    },
                }}
                open={open}
                aria-labelledby="alert-dialog-title"
                aria-describedby="alert-dialog-description"
                fullWidth
            >
                <DialogTitle id="alert-dialog-title">You are about to be logged out!</DialogTitle>
                <DialogContent>
                    <DialogContentText id="alert-dialog-description">
                        Stay logged in to keep working?
                    </DialogContentText>
                </DialogContent>
                <DialogActions>
                    <Button color={"secondary"} variant="outlined" onClick={() => handleClose(false)} color="primary">
                        No
                    </Button>
                    <Button color={"primary"} variant="contained" onClick={() => handleClose(true)} color="primary"
                            autoFocus>
                        Yes
                    </Button>
                </DialogActions>
            </Dialog>
        </div>
    );
}
