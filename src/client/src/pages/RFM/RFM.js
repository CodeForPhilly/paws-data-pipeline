import React from 'react';
import {
    Container,
    Divider,
    FormControl,
    FormControlLabel,
    FormLabel,
    Paper,
    Radio,
    RadioGroup
} from '@material-ui/core';
import _ from 'lodash';
import Typography from "@material-ui/core/Typography";
import Grid from "@material-ui/core/Grid";
import Box from "@material-ui/core/Box";
import {makeStyles} from "@material-ui/styles";


const useStyles = makeStyles({});

export function RFM(props) {
    const classes = useStyles();

    const [labels, setLabels] = React.useState([]);
    const [selectedLabel, setSelectedLabel] = React.useState("");
    const [participants, setParticipants] = React.useState(undefined);

    React.useEffect(() => {
        (async () => {
            let labelsResponse = await fetch(`/api/rfm/labels`,
                {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': 'Bearer ' + props.access_token
                    }
                });
            labelsResponse = await labelsResponse.json();
            setLabels(labelsResponse.result);
        })();
    }, []);

    const handleLabelChange = async (event) => {
        setSelectedLabel(event.target.value);
        let participantsResponse = await fetch(`/api/rfm/${event.target.value}/100`,
            {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer ' + props.access_token
                }
            });
        participantsResponse = await participantsResponse.json();
        setParticipants(participantsResponse.result);
    };

    return (
        <Container maxWidth={"lg"}>
            <Box display="flex" justifyContent="center" pb={3}>
                <Typography variant={"h2"}>RFM Scores</Typography>
            </Box>
            <Grid container direction="row" justify={"flex-start"}>
                <Grid container item direction="column" xs={3}>
                    {_.isEmpty(labels) !== true &&
                    <Grid item>

                        <FormControl component="fieldset">
                            <FormLabel component="legend">RFM Labels</FormLabel>
                            <RadioGroup aria-label="labels" onChange={handleLabelChange}>
                                {
                                    _.map(labels, labelData => {
                                        return <FormControlLabel value={labelData.rfm_label} control={<Radio/>}
                                                                 label={<Paper variant="outlined" elevation={3}>
                                                                     <Typography style={{
                                                                         backgroundColor: labelData.rfm_color,
                                                                         color: labelData.rfm_text_color,
                                                                         padding: 3
                                                                     }}>
                                                                         {labelData.rfm_label}
                                                                     </Typography>
                                                                 </Paper>}/>
                                    })
                                }
                            </RadioGroup>
                        </FormControl>
                    </Grid>}
                </Grid>
                <Grid container item direction="column" xs={3}>
                    {participants &&
                    _.map(participants, participantRow => {
                        debugger;
                        return <Typography>
                            {participantRow.mobile}
                        </Typography>
                    })}
                </Grid>
            </Grid>
        </Container>

    );
}