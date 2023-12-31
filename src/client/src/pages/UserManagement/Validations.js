import * as Yup from 'yup';

export const DISALLOWED_WORDS = [
    'cat',
    'dog',
    'password',
    'philly',
    'paws',
]

export const buildNameValidation = () => {
    return Yup.string()
        .trim()
        .min(2, "Name must be at least 2 characters")
        .max(50, "Name cannot be more than 50 characters")
        .matches(/^(?!.*\s{2,})[a-zA-Z ]+$/, "Name must only contain letters and non-consecutive internal spaces")
        .required("Name is required")
}

export const buildUsernameValidation = () => {
    return Yup.string()
        .trim()
        .min(2, "Username must be at least 2 characters")
        .max(50, "Username cannot be more than 50 characters")
        .matches(/^[a-zA-Z0-9].*$/, "Username must begin with a letter or number")
        .matches(/^.*[a-zA-Z0-9]$/, "Username must end with a letter or number")
        .matches(/^(?!.*?__)[a-zA-Z0-9_]+$/, "Username must contain only alphanumeric characters and non-consecutive underscores")
}

export const buildRoleValidation = () => {
    return Yup.string()
        .trim()
        .oneOf(["user", "admin"], "Role must be one of the following: user/admin")
        .required("Role is required")
}

export const buildPasswordValidation = (username) => {
    return Yup.string()
        .required("Password is required")
        .test(
            "no-disallowed-words",
            "Password cannot include 'dog', 'cat', 'password', 'philly', 'paws', or your username",
            (value, context) => {
                if (!value) {
                    return true;
                }

                const lowercasePassword = value.toLowerCase();
                const lowercaseUsername = username || context.parent.username.toLowerCase()
                return [...DISALLOWED_WORDS, lowercaseUsername].every((word) => !lowercasePassword.includes(word))
            })
        .matches(/^[a-zA-Z0-9!@#$%^*]+$/, "Password can only contain numbers, letters, and the following symbols: !@#$%^*")
        .min(12, "Password must contain at least 12 characters")
        .max(36, "Password must be 36 characters or less")
}
