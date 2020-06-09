export function onChartReady(chart, google) {
    let self = this;
    google.visualization.events.addListener(chart, "ready", function () {
        self.png = chart.getImageURI();
    });
}

//Print the Graph
export function print(title_graph= "", tp_name = "") {
    let WinPrint = window.open(
        "",
        "",
        "left=0,top=0,width=1000,height=900,toolbar=0,scrollbars=0,status=0"
    );
    WinPrint.document.write("<html><head>");
    WinPrint.document.write(
        "<link rel= \"stylesheet\" href= \"/css/print.css\">"
    );
    WinPrint.document.write("</head><body>");
    WinPrint.document.write("<img src=\"" + this.png + "\">");
    if (tp_name !== "") {
        WinPrint.document.write("<h1>" + title_graph + " - " + tp_name + "</h1>");
    }
    WinPrint.document.write("</body></html>");
    WinPrint.document.close();
    WinPrint.focus();
    WinPrint.print();

}