import { Container } from "@material-ui/core";
import React from "react"

export default function NoRecords(props) {
    const { recordType } = props;

    return (
        <Container style={{ padding: "16px" }}>
            {`No ${recordType} records on file.`}
        </Container>
    );
}
