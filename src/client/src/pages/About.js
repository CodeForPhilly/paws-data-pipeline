import React from 'react';
import {Container, Divider} from '@material-ui/core';
import _ from 'lodash';
import Typography from "@material-ui/core/Typography";
import Grid from "@material-ui/core/Grid";

const DEVELOPERS = [
    "Uri Rotem",
    "Cris Simpson",
    "Ben Bucior",
    "Stephen Poserina",
    "Mike Crnkovich",
    "Mike Damert",
    "Dave Salorio",
    "Mike Bailey",
    "Donna St. Louis",
    "Joe Illuminati",
    "Andrew Bishop",
    "Akshat Vas",
    "Dan Kelley",
    "Osman Sabahat",
    "Stephen Carroll",
    "Diego Delgado",
    "Carlos Dominguez",
    "Benjamin Deck",
    "Sam Lufi",
    "Ruthie Fields",
]

const PROJECT_MANAGERS = [
    "JW Truver",
    "Daniel Romero",
    "Eudora Linde",
    "Meg Niman"
]

const PROJECT_LEADS = [
    "Karla Fettich",
    "Chris Kohl"
]

const EXTERNAL_COLLABORATORS = [
    "Weston Welch",
    "Tan Tan Chen",
    "Faith Benamy",
    "Jesse",
    "Chris Alfano",
    "Josephine Dru",
]

const SUPPORTERS = [
    "Code for Philly",
    "Linode"
]

const getList = (listName) => {
    return (
        <ul>
            {_.map(listName, item => {
                return (<li>
                        <Typography>
                            {item}
                        </Typography>
                    </li>
                )
            })}
        </ul>
    );
};


export default function About() {
    return (
        <Container maxWidth={"md"} style={{"padding": "1em"}}>
            <Grid container direction="column" spacing={1}>

                <Grid item>
                    <Typography variant={"h2"}>
                        <a href="https://codeforphilly.org/projects/paws_data_pipeline" target="_blank"
                           rel="noopener noreferrer">
                            The PAWS Data Pipeline
                        </a>
                    </Typography>
                </Grid>
                <Grid item>
                    <Typography>
                        The PAWS data pipeline (PDP) is community-driven and developed software that serves the
                        Philadelphia Animal Welfare Society (PAWS), Philadelphia’s largest animal rescue partner
                        and no-kill animal shelter. It is a project that began on Nov 24, 2019 and is being built
                        through a volunteer effort coordinated by Code for Philly. PDP is free and open source
                        software. The volunteers that have worked on this project come from diverse backgrounds,
                        but are connected through a shared love for animals and a passion for technology.
                    </Typography>
                </Grid>
                <Grid item>
                    <Divider/>
                </Grid>
                <Grid item>
                    <Typography>{_.size(DEVELOPERS) + _.size(PROJECT_MANAGERS) + _.size(PROJECT_LEADS) + _.size(EXTERNAL_COLLABORATORS)} individuals and {_.size(SUPPORTERS)} organisations supported and contributed to the PDP between
                        2019/11/24 and 2023/06/13:</Typography>
                </Grid>
                <Grid item>
                    <Typography variant={"h3"}>Developers</Typography>
                </Grid>
                {getList(DEVELOPERS)}
                <Grid item>
                    <Typography variant={"h3"}>Project Managers</Typography>
                </Grid>
                {getList(PROJECT_MANAGERS)}
                <Typography variant={"h3"}>Project leads</Typography>
                {getList(PROJECT_LEADS)}
                <Typography variant={"h3"}>External collaborators and supporters</Typography>
                {getList(EXTERNAL_COLLABORATORS)}
                <Typography variant={"h3"}>Organisations providing support</Typography>
                {getList(SUPPORTERS)}
            </Grid>
        </Container>

    );
}