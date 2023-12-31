import {
    FormControlLabel,
    Radio,
    RadioGroup,
} from "@material-ui/core";
import React from "react";

const UserRoles = {
    Admin: "admin",
    User: "user",
};

const options = [
    {
        label: "Admin",
        value: UserRoles.Admin,
    },
    {
        label: "User",
        value: UserRoles.User,
    },
];

export default function RolesRadioGroup(props) {
    const { register, user } = props;
    const [selectedRole, setSelectedRole] = React.useState(user ? user.role : undefined);

    React.useEffect(() => {
        setSelectedRole(user ? user.role : null);
    }, [user]);

    const generateRadioOptions = () => {
        return options.map((option) => (
            <FormControlLabel
                key={option.value}
                value={option.value}
                label={option.label}
                control={<Radio />}
                checked={selectedRole === option.value}
                onClick={(() => setSelectedRole(option.value))}
                {...register("role")}
            />
        ));
    };

    return (
        <RadioGroup
            row
            name="role"
            {...register("role")}
        >
            {generateRadioOptions()}
        </RadioGroup>
    );
};
