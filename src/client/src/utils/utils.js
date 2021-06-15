import moment from "moment";

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