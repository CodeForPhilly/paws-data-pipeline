import React from 'react';
import NewUserDialog from './NewUserDialog';

export const DialogTypes = {
    NewUser: 'new-user',
}

export default function UserDialog(props) {
    const { onClose, type, token } = props;

    switch (type) {
        case DialogTypes.NewUser:
            return (
                <NewUserDialog
                    onClose={onClose}
                    token={token}
                    open
                >
                    "Hello"
                </NewUserDialog>
            )
        default:
            return null
    }
}