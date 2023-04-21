import React from 'react';
import NewUserDialog from './NewUserDialog';

export const DialogTypes = {
    NewUser: 'new-user',
}

export default function UserDialog(props) {
    const { notifyResult, onClose, type, token, updateUsers } = props;

    switch (type) {
        case DialogTypes.NewUser:
            return (
                <NewUserDialog
                    notifyResult={notifyResult}
                    onClose={onClose}
                    token={token}
                    updateUsers={updateUsers}
                >
                    "Hello"
                </NewUserDialog>
            )
        default:
            return null
    }
}