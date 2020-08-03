import React from 'react';

/* Handles the visibility of each tab. By checking index against selected value in parent component */
function TabPanel (props) {
    const { children, value, index } = props;

    return (
        <div className="tab-panel" role="tabpanel" hidden={value !== index} id={`upload-download-reports-tab-${index}`}>
          {children}
        </div>

    )

}

export default TabPanel;