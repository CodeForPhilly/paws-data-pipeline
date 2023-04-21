import React from 'react';
import ChangePasswordDialog from './ChangePasswordDialog';
import NewUserDialog from './NewUserDialog';
import UpdateUserDialog from './UpdateUserDialog';

export const DialogTypes = {
    NewUser: 'new-user',
    UpdateUser: 'update-user',
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
        case DialogTypes.UpdateUser:
            return (
                <UpdateUserDialog
                    notifyResult={notifyResult}
                    onClose={onClose}
                    token={token}
                    updateUsers={updateUsers}
                    user={selectedUser}
                />
            )
        case DialogTypes.ChangePassword:
            return (
                <ChangePasswordDialog
                    notifyResult={notifyResult}
                    onClose={onClose}
                    token={token}
                    user={selectedUser}
                />
            )
        default:
            return null
    }
}