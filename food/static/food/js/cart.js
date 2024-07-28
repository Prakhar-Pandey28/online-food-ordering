// Define constants
const HOURS = 24;
const MILLISECONDS_IN_HOUR = 60 * 60 * 1000;

// Handle localStorage clearing
const now = new Date().getTime();
let stepTime = localStorage.getItem('stepTime');

if (stepTime === null) {
    localStorage.setItem('stepTime', now);
} else {
    if (now - stepTime > HOURS * MILLISECONDS_IN_HOUR) {
        localStorage.clear();
        localStorage.setItem('stepTime', now);
    }
}

// Initialize cart data
let pizzaOrders = JSON.parse(localStorage.getItem("pizzaOrders")) || [];
let burgerOrders = JSON.parse(localStorage.getItem("burgerOrders")) || [];
let pizzaTotal = parseFloat(localStorage.getItem("pizzaTotal")) || 0;
let burgerTotal = parseFloat(localStorage.getItem("burgerTotal")) || 0;

// Update cart display
const cart = document.querySelector("#cart");
if (cart) {
    cart.innerHTML = pizzaOrders.length + burgerOrders.length;
}

// Add pizza to cart
function addPizza(id) {
    const pizzaName = document.querySelector("#piz" + id).textContent;
    const price = parseFloat(document.querySelector(`input[name="pizza${id}"]:checked`).value);

    pizzaOrders.push({ name: pizzaName, price: price });
    pizzaTotal += price;
    localStorage.setItem("pizzaOrders", JSON.stringify(pizzaOrders));
    localStorage.setItem("pizzaTotal", pizzaTotal);
    updateCart();
}

// Add burger to cart
function addBurger(id) {
    const burgerName = document.querySelector("#burg" + id).textContent;
    const price = parseFloat(document.querySelector(`input[name="burger${id}"]:checked`).value);

    burgerOrders.push({ name: burgerName, price: price });
    burgerTotal += price;
    localStorage.setItem("burgerOrders", JSON.stringify(burgerOrders));
    localStorage.setItem("burgerTotal", burgerTotal);
    updateCart();
}

// Update cart display
function updateCart() {
    if (cart) {
        cart.innerHTML = pizzaOrders.length + burgerOrders.length;
    }
    updateCartDisplay();
}

// Update cart display content
function updateCartDisplay() {
    const pCart = document.querySelector("#pcart");
    const pTotal = document.querySelector("#ptotal");
    const bCart = document.querySelector("#bcart");
    const bTotal = document.querySelector("#btotal");
    const overallTotal = document.querySelector("#overallTotal");

    if (pCart) {
        pCart.innerHTML = "";
        pizzaOrders.forEach((order, index) => {
            pCart.innerHTML += `<li>${order.name} - $${order.price.toFixed(2)} <button onclick="removePizza(${index})">Remove</button></li>`;
        });
        if (pTotal) {
            pTotal.innerHTML = `Total: $${pizzaTotal.toFixed(2)}`;
        }
    }

    if (bCart) {
        bCart.innerHTML = "";
        burgerOrders.forEach((order, index) => {
            bCart.innerHTML += `<li>${order.name} - $${order.price.toFixed(2)} <button onclick="removeBurger(${index})">Remove</button></li>`;
        });
        if (bTotal) {
            bTotal.innerHTML = `Total: $${burgerTotal.toFixed(2)}`;
        }
    }

    if (overallTotal) {
        overallTotal.innerHTML = `Total: $${(pizzaTotal + burgerTotal).toFixed(2)}`;
    }
}

// Remove pizza from cart
function removePizza(index) {
    pizzaTotal -= pizzaOrders[index].price;
    pizzaOrders.splice(index, 1);
    localStorage.setItem("pizzaOrders", JSON.stringify(pizzaOrders));
    localStorage.setItem("pizzaTotal", pizzaTotal);
    updateCart();
}

// Remove burger from cart
function removeBurger(index) {
    burgerTotal -= burgerOrders[index].price;
    burgerOrders.splice(index, 1);
    localStorage.setItem("burgerOrders", JSON.stringify(burgerOrders));
    localStorage.setItem("burgerTotal", burgerTotal);
    updateCart();
}

// Place order
// Place order
// Place order
function placeOrder() {
    const note = document.querySelector("#note").value;
    const orders = [...pizzaOrders.map(order => ["Pizza", order.name, order.price]), ...burgerOrders.map(order => ["Burger", order.name, order.price])];
    const bill = pizzaTotal + burgerTotal;

    fetch('/create-payment/', {  // Ensure this path matches the URL defined in Django
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')  // Function to get CSRF token
        },
        body: JSON.stringify({
            note: note,
            orders: orders,
            bill: bill
        })
    }).then(response => response.json())
      .then(data => {
          console.log(data); // Log the response data
          if (data.status === 'success') {
              // Redirect to the payment gateway
              window.location.href = data.payment_url;
          } else {
              alert('Failed to create payment.');
          }
      }).catch(error => {
          console.error('Error:', error); // Log any errors
          alert('An error occurred while processing the payment.');
      });
}
// Helper function to get CSRF token from cookies
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

updateCart();
