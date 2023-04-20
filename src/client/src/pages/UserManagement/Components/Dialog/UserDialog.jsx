import React from 'react';
import NewUserDialog from './NewUserDialog';

export const DialogTypes = {
    NewUser: 'new-user',
}

export default function UserDialog(props) {
    const { onClose, type } = props;

    switch (type) {
        case DialogTypes.NewUser:
            return (
                <NewUserDialog
                    onClose={onClose}
                    open
                >
                    "Hello"
                </NewUserDialog>
            )
        default:
            return null
    }
}