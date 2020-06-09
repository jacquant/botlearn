export function tooltipGenerator(errors){
    let chartData = []
    errors.forEach(error => {
        let text_tooltip = `<b> ${error.code} </b><br>Nombre d'erreurs: ${error.counter} <br>`;
        if (error.counter > 2) {
            text_tooltip += generate_tooltip_example([1, 2, 3], error.submissions_list);
        } else if (error.counter === 0) {
            text_tooltip += "Aucun exemple disponible";
        } else {
            text_tooltip += generate_tooltip_example(Array.from({length: error.submissions_list.length}, (v, k) => k + 1), error.submissions_list);
        }
        chartData.push([error.code, error.counter, text_tooltip]);
    });
    return chartData
}

function generate_tooltip_example(range, submissions_list) {
    return range.map(i => `<a href='/solution?id=${submissions_list[0]}'>  ${i} ° Voir exemple</a>`).join("<br>");
}