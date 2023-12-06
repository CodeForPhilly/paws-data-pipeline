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
                    onClose={onClose}
                    token={token}
                    updateUsers={updateUsers}
                />
            )
        case DialogTypes.UpdateUser:
            return (
                <UpdateUserDialog
                    onClose={onClose}
                    token={token}
                    updateUsers={updateUsers}
                    user={selectedUser}
                />
            )
        case DialogTypes.ChangePassword:
            return (
                <ChangePasswordDialog
                    onClose={onClose}
                    token={token}
                    user={selectedUser}
                />
            )
        default:
            return null
    }
}
