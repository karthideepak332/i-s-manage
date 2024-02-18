// pdf_generator.js

function generate_pdf(data) {
    var pdf = new jsPDF();
    pdf.text(10, 10, "Production Report");

    // Add data to the PDF
    var y = 20;
    data.forEach(function(row) {
        var x = 10;
        for (var key in row) {
            pdf.text(x, y, key + ": " + row[key]);
            y += 10;
        }
        y += 10; // Add some space between rows
    });

    // Save the PDF
    pdf.save("production_report.pdf");
}
