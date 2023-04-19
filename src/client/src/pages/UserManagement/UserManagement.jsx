import {
    Backdrop,
    Box,
    CircularProgress,
    Container,
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
import UserRow from './Components/UserRow';

export default function UserManagement(props) {
    const [users, setUsers] = React.useState(undefined);
    const [isLoading, setIsLoading] = React.useState(undefined);
    const { access_token: token } = props;

    React.useEffect(() => {
        setIsLoading(true);
        fetchUsers({ token })
            .then((data) => {
                setUsers(data)
            })
        setIsLoading(false);
    }, [token]);

    return (
        <Container>1
            <Box display="flex" justifyContent="center" pb={3}>
                <Typography variant={"h2"} >User Management</Typography>
            </Box>
            {isLoading &&
                <Backdrop open={true}>
                    <CircularProgress size={60} />
                </Backdrop>
            }
            {!isLoading && users &&
                <Paper elevation={1} style={{ "padding": "2em" }}>
                    <Table>
                        <TableHead>
                            <TableRow>
                                <TableCell>Username</TableCell>
                                <TableCell>Full Name</TableCell>
                                <TableCell>Role</TableCell>
                                <TableCell>Active</TableCell>
                            </TableRow>
                        </TableHead>
                        <TableBody>
                            {_.map(users, user => {
                                return <UserRow user={user} key={user.username} />
                            })}
                        </TableBody>
                    </Table>
                </Paper>
            }
        </Container>
    )
}
