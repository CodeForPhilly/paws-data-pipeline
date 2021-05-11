import React from 'react';
import { Container } from '@material-ui/core';

export default function About(props) {
  return (
    <Container>
      <Container style={{ "padding": "1em" }}>
        <h2>
          <a href="https://codeforphilly.org/projects/paws_data_pipeline" target="_blank">
            The PAWS Data Pipeline
          </a>
        </h2>
        <p>
          The PAWS data pipeline (PDP) is community-driven and developed software that serves the 
          Philadelphia Animal Welfare Society (PAWS), Philadelphia’s largest animal rescue partner 
          and no-kill animal shelter. It is a project that began on Nov 24, 2019 and is being built 
          through a volunteer effort coordinated by Code for Philly. PDP is free and open source 
          software. The volunteers that have worked on this project come from diverse backgrounds, 
          but are connected through a shared love for animals and a passion for technology.
        </p>
        <p>24 individuals and 2 organisations supported and contributed to the PDP between 2019/11/24 and 2021/05/01:</p>
        <h3>Developers</h3>
        <ul>
          <li>Uri Rotem</li>
          <li>Cris Simpson</li>
          <li>Ben Bucior</li>
          <li>Stephen Poserina</li>
          <li>Mike Crnkovich</li>
          <li>Mike Damert</li>
          <li>Dave Salorio</li>
          <li>Mike Bailey</li>
          <li>Donna St. Louis</li>
          <li>Joe Illuminati</li>
          <li>Andrew Bishop</li>
          <li>Akshat Vas</li>
          <li>Dan Kelley</li>
        </ul>
        <h3>Project managers</h3>
        <ul>
          <li>JW Truver</li>
          <li>Daniel Romero</li>
          <li>Eudora Linde</li>
          <li>Meg Niman</li>
        </ul>
        <h3>Project leads</h3>
        <ul>
          <li>Karla Fettich</li>
          <li>Chris Kohl</li>
        </ul>
        <h3>External collaborators and supporters</h3>
        <ul>
          <li>Weston Welch</li>
          <li>Tan Tan Chen</li>
          <li>Faith Benamy</li>
          <li>Jesse</li>
          <li>Chris Alfano</li>
        </ul>
        <h3>Organisations providing support</h3>
        <ul>
          <li>Code for Philly</li>
          <li>Linode</li>
        </ul>
      </Container>
    </Container>
  );
}