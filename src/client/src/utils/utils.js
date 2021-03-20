
export function formatPhoneNumber(phoneNumberString) {
    let retVal;

    if(phoneNumberString) {
        const match = phoneNumberString.match(/^(\d{3})(\d{3})(\d{4})$/)

        if (match) {
            retVal = '(' + match[1] + ') ' + match[2] + '-' + match[3];
        }
    }

    return retVal;
}