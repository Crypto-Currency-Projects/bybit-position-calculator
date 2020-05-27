window.addEventListener("load", () => {
    document.getElementById("calculate-long").addEventListener("click", () => {
        calculate("LONG");
    });
    document.getElementById("calculate-short").addEventListener("click", () => {
        calculate("SHORT");
    });
});

function out(n) {
    var output = document.getElementById("output");
    output.innerHTML = "";
    console.log(n);
    if (n["message"] != "OK") {
        output.innerHTML = `<tr><td class="color-red">${n["message"]}</td></tr>`;
    } else {
        var data = n["data"];
        var x = `<tr><th>Symbol</th><td>${data["symbol"][0] + data["symbol"][1]}</td></tr>`;
        x += `<tr><th>Total Contracts</th><td>${data["totalContracts"]}</td></tr>`;
        x += `<tr><th>Average Entry Price</th><td>${data["averageEntryPrice"]}</td></tr>`;
        x += `<tr><th>Max Leverage</th><td>${data["leverage"]}x</td></tr>`;
        x += `<tr><th colspan="2">Individual Orders</th></tr>`;
        for (var i of data["orders"]) {
            x += `<tr><td colspan="2">Price: ${i["price"]} Qty: ${i["qty"]}</td></tr>`;
        }
        output.innerHTML = x
    }
}

function calculate(side) {
    var balance = document.getElementById("balance").value;
    var symbol = document.getElementById("symbol").value;
    var risk = document.getElementById("risk").value;
    var start = document.getElementById("start").value;
    var end = document.getElementById("end").value;
    var stopLoss = document.getElementById("stopLoss").value;
    var orders = document.getElementById("orders").value;

    var range;
    if (start > end)
        range = [end, start];
    else
        range = [start, end];

    eel.calculate(balance, symbol, side, risk, range, stopLoss, orders)(out);
}
