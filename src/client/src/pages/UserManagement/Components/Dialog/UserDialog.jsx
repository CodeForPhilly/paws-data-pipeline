import React from 'react';
import ChangePasswordDialog from './ChangePasswordDialog';
import NewUserDialog from './NewUserDialog';

export const DialogTypes = {
    NewUser: 'new-user',
    ChangePassword: 'change-password',
}

export default function UserDialog(props) {
    const {
        notifyResult,
        onClose,
        selectedUser,
        type,
        token,
        updateUsers
    } = props;

    switch (type) {
        case DialogTypes.NewUser:
            return (
                <NewUserDialog
                    notifyResult={notifyResult}
                    onClose={onClose}
                    token={token}
                    updateUsers={updateUsers}
                />
            )
        case DialogTypes.ChangePassword:
            return (
                <ChangePasswordDialog
                    notifyResult={notifyResult}
                    onClose={onClose}
                    user={selectedUser}
                    token={token}
                />
            )
        default:
            return null
    }
}