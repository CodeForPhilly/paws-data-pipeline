import React, { useState } from 'react';
import PropTypes from 'prop-types';
import { useHistory } from "react-router-dom";


export default function Logout({ setToken }) {
    
    setToken(null);
    let history = useHistory();
    history.push('/')

    return (
        <div></div>
    )
}

Logout.propTypes = {
    setToken: PropTypes.func.isRequired
};