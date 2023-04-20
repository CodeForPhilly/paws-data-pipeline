import { yupResolver } from "@hookform/resolvers/yup";
import { Button, Dialog, DialogActions, DialogContent, DialogTitle, TextField, Typography } from '@material-ui/core';
import React from 'react';
import { useForm } from 'react-hook-form';
import * as Yup from 'yup';
import { createUser } from "../../../../utils/api";
import { buildNameValidation, buildPasswordValidation, buildRoleValidation, buildUsernameValidation } from '../../Validations';


export default function NewUserDialog(props) {
    const { onClose, token } = props;

    const validationSchema = Yup.object().shape({
        name: buildNameValidation(),
        username: buildUsernameValidation(),
        role: buildRoleValidation(),
        password: buildPasswordValidation(),
        confirmPassword: Yup.string().oneOf([Yup.ref("password")], "Passwords must match"),
    });

    const { register, handleSubmit, formState: { errors }, reset } = useForm({
        resolver: yupResolver(validationSchema),
    });

    const onSubmitHandler = (data) => {
        const { username, name: full_name, role, password } = data;

        createUser({
            username,
            full_name,
            role,
            password
        }, token)
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
                        variant="standard"
                        fullWidth
                    />
                    {errors.username &&
                        <Typography color="error">{errors.username.message}</Typography>
                    }
                    <TextField
                        {...register("role")}
                        margin="dense"
                        id="role-input"
                        label="Role - user/editor/admin"
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