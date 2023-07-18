import { yupResolver } from "@hookform/resolvers/yup";
import {
    Button,
    Dialog,
    DialogActions,
    DialogContent,
    DialogTitle,
    TextField,
    Typography
} from '@material-ui/core';
import React from 'react';
import { useForm } from 'react-hook-form';
import * as Yup from 'yup';
import { createUser } from "../../../../utils/api";
import {
    buildNameValidation,
    buildPasswordValidation,
    buildRoleValidation,
    buildUsernameValidation
} from '../../Validations';


export default function NewUserDialog(props) {
    const [responseError, setResponseError] = React.useState(undefined);
    const {
        onClose,
        notifyResult,
        token,
        updateUsers
    } = props;

    const validationSchema = Yup.object().shape({
        name: buildNameValidation(),
        username: buildUsernameValidation(),
        role: buildRoleValidation(),
        password: buildPasswordValidation(),
        confirmPassword: Yup.string().oneOf([Yup.ref("password")], "Passwords must match"),
    });

    const { register, handleSubmit, formState: { errors }, trigger } = useForm({
        resolver: yupResolver(validationSchema),
    });

    const onSubmitHandler = (data) => {
        setResponseError(null);

        const newUser = {
            username: data.username,
            full_name: data.name,
            role: data.role,
            password: data.password
        };

        createUser(newUser, token)
            .then((res) => {
                if (res.indexOf("duplicate key") > -1) {
                    setResponseError(`User with username ${data.username} already exists`)
                } else {
                    notifyResult({ success: true, message: `New user ${res} created successfully` });
                    updateUsers(newUser);
                    onClose();
                }
            })
            .catch(e => console.warn(e))
    }

    return (
        <Dialog
            hideBackdrop
            fullWidth
            open
        >
            <DialogTitle style={{ fontSize: "20px" }}>Create New User</DialogTitle>
            <form onSubmit={handleSubmit(onSubmitHandler)}>
                <DialogContent>
                    <TextField
                        {...register("name")}
                        margin="dense"
                        id="name-input"
                        label="Name"
                        onBlur={() => trigger("name")}
                        variant="standard"
                        autoFocus
                        fullWidth
                    />
                    {errors.name &&
                        <Typography color="error">{errors.name.message}</Typography>
                    }
                    <TextField
                        {...register("username")}
                        margin="dense"
                        id="username-input"
                        label="Username"
                        onBlur={() => trigger("username")}
                        variant="standard"
                        fullWidth
                    />
                    {(responseError || errors.username) && // This is a little janky... Could be improved upon.
                        <Typography color="error">{responseError || errors.username.message}</Typography>
                    }
                    <TextField
                        {...register("role")}
                        margin="dense"
                        id="role-input"
                        label="Role - user/editor/admin"
                        onBlur={() => trigger("role")}
                        variant="standard"
                        fullWidth
                    />
                    {errors.role &&
                        <Typography color="error">{errors.role.message}</Typography>
                    }
                    <TextField
                        {...register("password")}
                        margin="dense"
                        id="password-input"
                        label="Password"
                        onBlur={() => trigger("password")}
                        type="password"
                        fullWidth
                    />
                    {errors.password &&
                        <Typography color="error">{errors.password.message}</Typography>
                    }
                    <TextField
                        {...register("confirmPassword")}
                        margin="dense"
                        id="confirm-password-input"
                        label="Confirm Password"
                        onBlur={() => trigger("confirmPassword")}
                        type="password"
                        fullWidth
                    />
                    {errors.confirmPassword &&
                        <Typography color="error">{errors.confirmPassword.message}</Typography>
                    }
                    <DialogActions>
                        <Button
                            onClick={onClose}
                        >
                            Cancel
                        </Button>
                        <Button
                            type="submit"
                        >
                            Submit
                        </Button>
                    </DialogActions>
                </DialogContent>
            </form>
        </Dialog>
    )
}
