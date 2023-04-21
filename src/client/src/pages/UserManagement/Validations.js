import * as Yup from 'yup';

export const DISALLOWED_WORDS = [
    'cat',
    'dog',
    'password',

]

export const buildNameValidation = () => {
    return Yup.string()
        .min(2, "Name must be at least 2 characters")
        .matches(/^[A-Za-z]+$/, "Name must only contain letters")
        .required("Name is required")
}

export const buildUsernameValidation = () => {
    return Yup.string()
        .min(2, "Username must be at least 2 characters")
        .matches(/^[a-zA-Z0-9].*$/, "Username must begin with a letter")
        .matches(/^.*[a-zA-Z0-9]$/, "Username must end with a letter")
        .matches(/^(?!.*?__)[a-zA-Z0-9_]+$/, "Username must contain only alphanumeric characters and non-consecutive underscores")
}

export const buildRoleValidation = () => {
    return Yup.string()
        .oneOf(["user", "editor", "admin"], "Role must be one of the following: user/editor/admin")
        .required("Role is required")
}

export const buildPasswordValidation = (username) => {
    return Yup.string()
        .test(
            "no-disallowed-words",
            "Password cannot include 'dog', 'cat', 'password', or your username",
            (value, context) => {
                if (!value) {
                    return true;
                }

                const lowercasePassword = value.toLowerCase();
                const lowercaseUsername = username || context.parent.username.toLowerCase()
                return [...DISALLOWED_WORDS, lowercaseUsername].every((word) => !lowercasePassword.includes(word))
            })
        .min(12, "Password must contain at least 12 letters")
        .max(36, "Password must be 36 characters or less")
}
