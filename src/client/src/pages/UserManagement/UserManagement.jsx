import {
    Backdrop,
    Button,
    CircularProgress,
    Container,
    Grid,
    Paper,
    Table,
    TableBody,
    TableCell,
    TableHead,
    TableRow,
    Typography
} from '@material-ui/core';
import _ from 'lodash';
import React from 'react';
import { fetchUsers } from '../../utils/api';
import UserDialog, { DialogTypes } from './Components/Dialog/UserDialog';
import UserRow from './Components/UserRow';

export default function UserManagement(props) {
    const [users, setUsers] = React.useState(undefined);
    const [isLoading, setIsLoading] = React.useState(undefined);
    const [dialogOpen, setDialogOpen] = React.useState(false);
    const [dialogType, setDialogType] = React.useState(undefined)
    const [selectedUser, setSelectedUser] = React.useState(undefined);
    const { access_token: token } = props;

    React.useEffect(() => {
        setIsLoading(true);
        fetchUsers({ token })
            .then((data) => {
                setUsers(data)
            })
        setIsLoading(false);
    }, [token]);
    const updateUsers = (newOrUpdatedUser) => {
        setUsers(prevUsers => {
            const existingUserIndex = _.findIndex(users, existingUser => {
                return existingUser.username === newOrUpdatedUser.username;
            })

            if (existingUserIndex >= 0) {
                const updatedUsers = [...prevUsers];
                updatedUsers[existingUserIndex] = newOrUpdatedUser;
                return updatedUsers;
            } else {
                return [...users, newOrUpdatedUser];
            }
        })
    }

    const openDialog = (opts) => {
        setSelectedUser(opts.user);
        setDialogType(opts.type);
        setDialogOpen(true);
    }

    const closeDialog = React.useCallback(() => {
        setDialogOpen(false);
        setDialogType(null);
        setSelectedUser(null);
    }, [setDialogOpen, setDialogType, setSelectedUser])

    React.useEffect(() => {
        const handleEscape = (event) => {
            if (event.keyCode === 27) {
                closeDialog();
            }
        }

        document.addEventListener('keydown', handleEscape);

        return () => {
            document.removeEventListener('keydown', handleEscape);
        };
    }, [closeDialog])

    return (
        <Container>
            {
                /*
                    The following Grid is pretty gross. I spent an inordinate amount of time trying
                    to align the button correctly with MUI stuff. Could definitely use improvement.
                */
            }
            <Grid display="flex" direction="row" justify="space-around" style={{ paddingBottom: '24px' }} container>
                <Grid item />
                <Grid item>
                    <Typography variant={"h2"} >User Management</Typography>
                </Grid >
                <Grid item>
                    <Button color="primary" variant="contained" onClick={() => openDialog({ type: DialogTypes.NewUser })}>
                        New
                    </Button>
                </Grid>
            </Grid >
            {isLoading &&
                <Backdrop open={true}>
                    <CircularProgress size={60} />
                </Backdrop>
            }
            {!isLoading && users &&
                <Paper elevation={1} style={{ padding: "2em" }}>
                    <Table>
                        <TableHead>
                            <TableRow>
                                <TableCell>Full Name</TableCell>
                                <TableCell>Username</TableCell>
                                <TableCell>Role</TableCell>
                                <TableCell>Active</TableCell>
                                <TableCell></TableCell>
                                <TableCell></TableCell>
                            </TableRow>
                        </TableHead>
                        <TableBody>
                            {_.map(users, user => {
                                return <UserRow user={user} openDialog={openDialog} key={user.username} />
                            })}
                        </TableBody>
                    </Table>
                </Paper>
            }
            {dialogOpen &&
                <UserDialog
                    onClose={closeDialog}
                    selectedUser={selectedUser}
                    token={token}
                    type={dialogType}
                    updateUsers={updateUsers}
                />
            }
        </Container >

    )
}
