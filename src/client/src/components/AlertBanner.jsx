import React from "react";

import { Alert } from "@material-ui/lab";
import useAlert from "../hooks/useAlert";

const AlertBanner = () => {
    const { text, type, setAlert } = useAlert();

    if (text && type) {
        return (
            <Alert
                onClose={() => setAlert(null)}
                severity={type}
                sx={{
                    position: "absolute",
                    zIndex: 10,
                }}
            >
                {text}
            </Alert>
        );
    } else {
        return <></>;
    }
};

export default AlertBanner;
