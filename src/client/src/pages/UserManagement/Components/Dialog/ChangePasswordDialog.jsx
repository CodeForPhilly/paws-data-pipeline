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
import { updateUser } from "../../../../utils/api";
import { buildPasswordValidation } from '../../Validations';
import useAlert from "../../../../hooks/useAlert";


export default function ChangePasswordDialog(props) {
    const {
        onClose,
        token,
        user
    } = props;
    const { username } = user;
    const { setAlert } = useAlert();

    const validationSchema = Yup.object().shape({
        password: buildPasswordValidation(username),
        confirmPassword: Yup.string().oneOf([Yup.ref("password")], "Passwords must match"),
    });

    const { register, handleSubmit, formState: { errors }, trigger } = useForm({
        resolver: yupResolver(validationSchema),
    });

    const onSubmitHandler = (data) => {
        const { password } = data;

        updateUser({ username, password }, token)
            .then((res) => {
                if (res === "Updated") {
                    setAlert({ type: "success", text: `Password for user ${username} successfully changed!` });
                } else {
                    setAlert({ type: "error", text: res });
                }
            })
            .catch(e => {
                console.warn(e)
                setAlert({ type: "error", text: e })
            });
        onClose();
    }

    return (
        <Dialog
            hideBackdrop
            fullWidth
            open
        >
            <DialogTitle style={{ fontSize: "20px" }}>Change Password</DialogTitle>
            <form onSubmit={handleSubmit(onSubmitHandler)}>
                <DialogContent>
                    <Typography>
                        {`Fill out the fields below to update the password for user with username: ${user.username}.`}
                    </Typography>
                    <TextField
                        {...register("password")}
                        margin="dense"
                        id="password-input"
                        label="Password"
                        onBlur={() => trigger("password")}
                        type="password"
                        autoFocus
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
