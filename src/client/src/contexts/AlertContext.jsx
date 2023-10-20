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

    const setAlert = (text, type) => {
        setText(text);
        setType(type);

        if (type !== "error") {
            setTimeout(() => {
                setText("");
                setType("");
            }, ALERT_TIME);
        }
    };

    return (
        <AlertContext.Provider
            value={{
                text,
                type,
                setAlert,
            }}
        >
            {children}
        </AlertContext.Provider>
    );
};

export default AlertContext;
