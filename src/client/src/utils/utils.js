import moment from 'moment-timezone';

export function formatPhoneNumber(phoneNumberString) {
    let retVal;

    if (phoneNumberString) {
        const match = phoneNumberString.match(/^(\d{3})(\d{3})(\d{4})$/)

        if (match) {
            retVal = '(' + match[1] + ') ' + match[2] + '-' + match[3];
        }
    }

    return retVal;
}

export function getAnimalAge(epochTime) {
    let dateOfBirth = moment(epochTime * 1000);
    return moment().diff(dateOfBirth, 'years');
}

export function showAnimalAge(epochTime) {
    const age = getAnimalAge(epochTime)
    return (age === 1) ? `${age} year` : `${age} years`
}

export function formatTimestamp(timestamp) {
    const momentObj = moment.utc(timestamp);
    return momentObj.tz("America/New_York").format("MMMM Do YYYY, h:mm:ss a");
}

export function formatUploadType(data) {
    switch (data) {
        case 'last_volgistics_update':
            return 'Last Volgistics update:';
        case 'last_shelterluv_update':
            return 'Last Shelterluv update:';
        case 'last_salesforce_update':
            return 'Last Salesforce update:';
        default:
            break;
    }
}