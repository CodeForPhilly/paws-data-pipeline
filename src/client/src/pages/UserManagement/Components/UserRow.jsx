import {
    Button,
    TableCell,
    TableRow
} from "@material-ui/core";
import React from 'react';
import { DialogTypes } from "./Dialog/UserDialog";

export default function UserRow(props) {
    const { active, full_name: fullName, role, username } = props.user;
    const openDialog = props.openDialog;

    return (
        <TableRow>
            <TableCell>{fullName}</TableCell>
            <TableCell>{username}</TableCell>
            <TableCell>{role}</TableCell>
            <TableCell>{active === 'Y' ? 'Yes' : 'No'}</TableCell>
            <TableCell>
                <Button>
                    Update User
                </Button>
            </TableCell>
            <TableCell>
                <Button onClick={() => openDialog({ type: DialogTypes.ChangePassword, user: props.user })}>
                    Change Password
                </Button>
            </TableCell>
        </TableRow>
    )
}
