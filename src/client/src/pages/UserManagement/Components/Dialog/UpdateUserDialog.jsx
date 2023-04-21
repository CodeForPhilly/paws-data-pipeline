import { yupResolver } from "@hookform/resolvers/yup";
import {
    Button,
    Checkbox,
    Dialog,
    DialogActions,
    DialogContent,
    DialogTitle,
    FormControlLabel,
    TextField,
    Typography
} from '@material-ui/core';
import React from 'react';
import { useForm } from 'react-hook-form';
import * as Yup from 'yup';
import { updateUser } from "../../../../utils/api";
import { buildNameValidation, buildRoleValidation } from '../../Validations';


export default function UpdateUserDialog(props) {
    const {
        onClose,
        notifyResult,
        token,
        updateUsers,
        user
    } = props;
    const {
        username,
        full_name: name,
        role,
        active
    } = user;

    const validationSchema = Yup.object().shape({
        name: buildNameValidation(),
        role: buildRoleValidation(),
        active: Yup.boolean(),
    });

    const { register, handleSubmit, formState: { errors }, trigger } = useForm({
        resolver: yupResolver(validationSchema),
    });

    const onSubmitHandler = (data) => {
        const newUser = {
            username,
            full_name: data.name,
            role: data.role,
            active: data.active ? "Y" : "N"
        };

        updateUser(newUser, token)
            .then((res) => {
                if (res === "Updated") {
                    notifyResult({ success: true, message: `User ${username} updated successfully` });
                    updateUsers(newUser);
                    onClose();
                } else {
                    notifyResult({ success: false, message: res })
                }
            })
            .catch(e => {
                console.warn(e)
                notifyResult({ success: false, message: e })
            })
    }

    return (
        <Dialog
            hideBackdrop
            fullWidth
            open
        >
            <DialogTitle style={{ fontSize: "20px" }}>Update user</DialogTitle>
            <form onSubmit={handleSubmit(onSubmitHandler)}>
                <DialogContent>
                    <TextField
                        {...register("name")}
                        defaultValue={name}
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
                        defaultValue={username}
                        margin="dense"
                        id="username-input"
                        label="Username"
                        onBlur={() => trigger("username")}
                        variant="standard"
                        disabled
                        fullWidth
                    />
                    {(errors.username) &&
                        <Typography color="error">{errors.username.message}</Typography>
                    }
                    <TextField
                        {...register("role")}
                        defaultValue={role}
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
                    <FormControlLabel
                        control={
                            <Checkbox
                                {...register("active")}
                                defaultChecked={active === "Y" ? true : false}
                            />
                        }
                        label="Active"
                    />
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
