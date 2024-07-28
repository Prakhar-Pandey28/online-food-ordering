var hours = 24;
var now = new Date().getTime();
var stepTime = localStorage.getItem('stepTime');

if (stepTime == null) {
    localStorage.setItem('stepTime', now);
} else {
    if (now - stepTime > hours * 60 * 60 * 1000) {
        localStorage.clear();
        localStorage.setItem('stepTime', now);
    }
}

var orders = JSON.parse(localStorage.getItem("pizzaOrders")) || [];
var total = localStorage.getItem("pizzaTotal");

if (total === null || total === undefined) {
    localStorage.setItem("pizzaTotal", 0);
    total = 0;
} else {
    total = Number(total);
}

var cart = document.querySelector("#cart");
cart.innerHTML = orders.length;
