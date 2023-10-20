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
    const timerRef = React.useRef(null);

    const setAlert = ({ type, text }) => {
        setType(type);
        setText(text);

        if (timerRef.current) {
            clearTimeout(timerRef.current);
        }

        if (type !== "error") {
            timerRef.current = setTimeout(() => {
                setText("");
                setType("");
            }, ALERT_TIME);
        }
    };

    const clearAlert = () => {
        if (timerRef.current) {
            clearTimeout(timerRef.current);
        }

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
