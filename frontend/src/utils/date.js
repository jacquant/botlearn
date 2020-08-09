/**
 * Function to print the date correctly
 * @param {Date} date
 * @returns {String}
 * */
export function printDate(date) {
    const options = {
        year: "numeric", month: "long", day: "2-digit",
        hour: "2-digit", minute: "2-digit", second: "2-digit"
    };
    return new Intl.DateTimeFormat("fr-BE", options).format(date);
}
