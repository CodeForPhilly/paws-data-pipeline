import React from 'react';

const ALERT_TIME = 5000;
const initialState = {
    text: "",
    type: "",
};

const AlertContext = React.createContext({
    ...initialState,
    setAlert: () => {},
});

export const AlertProvider = ({ children }) => {
    const [text, setText] = React.useState("");
    const [type, setType] = React.useState("");

    const setAlert = ({ type, text }) => {
        setType(type);
        setText(text);

        if (type !== "error") {
            setTimeout(() => {
                setText("");
                setType("");
            }, ALERT_TIME);
        }
    };

    const clearAlert = () => {
        setType("");
        setText("");
    }

    return (
        <AlertContext.Provider
            value={{
                text,
                type,
                setAlert,
                clearAlert,
            }}
        >
            {children}
        </AlertContext.Provider>
    );
};

export default AlertContext;
