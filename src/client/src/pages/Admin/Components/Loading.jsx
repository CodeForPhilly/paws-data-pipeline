import React from "react";
import {
    Box,
    Backdrop,
    CircularProgress,
    Typography,
} from "@material-ui/core";

export default function Loading({ text, speed = 300 }) {
    const [content, setContent] = React.useState(text);

    React.useEffect(() => {
        const id = window.setInterval(() => {
            setContent((content) => {
                return content === `${text}...` ? text : `${content}.`;
            });
        }, speed);

        return () => window.clearInterval(id);
    }, [text, speed]);

    return (
        <Backdrop open={true}>
            <Box
                display="flex"
                flexDirection="column"
                justifyContent="center"
                alignItems="center"
            >
                <CircularProgress size={60} />
                {text &&
                    <Box paddingTop="16px">
                        <Typography>
                            {content}
                        </Typography>
                    </Box>
                }
            </Box>
        </Backdrop>
    );
}