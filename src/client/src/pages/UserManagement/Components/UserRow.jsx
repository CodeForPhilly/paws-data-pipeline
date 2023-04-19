import {
    TableCell,
    TableRow
} from "@material-ui/core";
import React from 'react';

export default function UserRow(props) {
    const { active, full_name: fullName, role, username } = props.user;

    return (
        <TableRow>
            <TableCell>{username}</TableCell>
            <TableCell>{fullName}</TableCell>
            <TableCell>{role}</TableCell>
            <TableCell>{active === 'Y' ? 'Yes' : 'No'}</TableCell>
        </TableRow>
    )
}
