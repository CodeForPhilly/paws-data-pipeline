import { Button, Dialog, DialogActions, DialogContent, DialogTitle, TextField } from '@material-ui/core';
import React from 'react';

export default function NewUserDialog(props) {
    const { onClose } = props;

    return (
        <Dialog
            hideBackdrop
            fullWidth
            open
        >
            <DialogTitle style={{ fontSize: '20px' }}>Create New User</DialogTitle>
            <DialogContent>
                <TextField
                    margin="dense"
                    id="full-name-input"
                    label="Full Name"
                    variant="standard"
                    autoFocus
                    fullWidth
                />
                <TextField
                    margin="dense"
                    id="username-input"
                    label="Username"
                    variant="standard"
                    fullWidth
                />
                <TextField
                    margin="dense"
                    id="role-input"
                    label="Role - user/editor/admin"
                    variant="standard"
                    fullWidth
                />
                <TextField
                    margin="dense"
                    id="password-input"
                    label="Password"
                    type="password"
                    fullWidth
                />
                <TextField
                    margin="dense"
                    id="confirm-password-input"
                    label="Confirm Password"
                    type="password"
                    fullWidth
                />
                <DialogActions>
                    <Button
                        onClick={onClose}
                    >
                        Cancel
                    </Button>
                    <Button
                    // type="submit"
                    >
                        Submit
                    </Button>
                </DialogActions>
            </DialogContent>
        </Dialog>
    )

}