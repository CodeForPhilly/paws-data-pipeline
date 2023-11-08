import React from "react";

import { Alert, AlertTitle } from "@material-ui/lab";
import useAlert from "../hooks/useAlert";
import { Typography } from "@material-ui/core";
import _ from "lodash";

const AlertBanner = () => {
    const { text, type, clearAlert } = useAlert();

    if (text && type) {
        return (
            <Alert onClose={() => clearAlert()} severity={type} spacing={2} >
                <AlertTitle>
                    <Typography variant="h6">{_.startCase(type)}</Typography>
                </AlertTitle>
                <Typography>{text}</Typography>
            </Alert>
        );
    } else {
        return <></>;
    }
};

export default AlertBanner;
