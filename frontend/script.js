let cart = [];
let products = [];

// Load products and render them with + - buttons
async function loadProducts() {
    const res = await fetch("http://localhost:5000/products");
    products = await res.json();

    const container = document.getElementById("products");
    container.innerHTML = '';

    products.forEach((p) => {
        const box = document.createElement("div");
        box.className = "product-box";

        const img = document.createElement("img");
        img.src = `assets/images/${p.name.toLowerCase()}.jpg`;
        img.alt = p.name;

        const name = document.createElement("p");
        name.textContent = p.name;

        const price = document.createElement("p");
        price.textContent = `$${p.price}`;

        const qtyWrapper = document.createElement("div");
        qtyWrapper.className = "quantity-controls";

        const minus = document.createElement("button");
        minus.textContent = "-";

        const qty = document.createElement("input");
        qty.type = "number";
        qty.value = 1;
        qty.min = 1;
        qty.className = "quantity-input";

        const plus = document.createElement("button");
        plus.textContent = "+";

        minus.onclick = () => {
            if (qty.value > 1) qty.value--;
        };

        plus.onclick = () => {
            qty.value++;
        };

        qtyWrapper.appendChild(minus);
        qtyWrapper.appendChild(qty);
        qtyWrapper.appendChild(plus);

        const addBtn = document.createElement("button");
        addBtn.textContent = "Add to Cart";
        addBtn.onclick = () => addToCart(p.id, parseInt(qty.value), p.name);

        box.appendChild(img);
        box.appendChild(name);
        box.appendChild(price);
        box.appendChild(qtyWrapper);
        box.appendChild(addBtn);

        container.appendChild(box);
    });
}

function addToCart(id, qty, name) {
    const existingIndex = cart.findIndex(item => item.id === id);
    if (existingIndex !== -1) {
        cart[existingIndex].qty += qty;
    } else {
        cart.push({ id, qty, name });
    }

    updateCartDisplay();
    updateTotal();
}

function removeFromCart(index) {
    cart.splice(index, 1);
    updateCartDisplay();
    updateTotal();
}

function updateCartDisplay() {
    const list = document.getElementById("cart-list");
    list.innerHTML = '';

    cart.forEach((item, index) => {
        const product = products.find(p => p.id == item.id);
        const total = (product.price * item.qty).toFixed(2);

        const li = document.createElement("li");
        li.textContent = `${item.name} ${item.qty} × $${product.price} = $${total} `;

        const plus = document.createElement("button");
        plus.textContent = "+";
        plus.onclick = () => {
            item.qty++;
            updateCartDisplay();
            updateTotal();
        };

        const minus = document.createElement("button");
        minus.textContent = "-";
        minus.onclick = () => {
            item.qty--;
            if (item.qty <= 0) cart.splice(index, 1);
            updateCartDisplay();
            updateTotal();
        };

        li.appendChild(plus);
        li.appendChild(minus);
        list.appendChild(li);
    });
}

function updateTotal() {
    let total = 0;
    cart.forEach(item => {
        const product = products.find(p => p.id == item.id);
        total += product.price * item.qty;
    });
    document.getElementById("total").textContent = total.toFixed(2);
}

let orderId = 1;
function placeOrder() {
    if (cart.length === 0) return;

    const orderIdElement = document.getElementById("order-id-result");
    orderIdElement.textContent = `Your Order ID is: ${orderId}`;
    orderId++;

    document.querySelectorAll("#cart-list button").forEach(btn => btn.disabled = true);
    document.querySelectorAll(".product-box button").forEach(btn => btn.disabled = true);
}

function checkStatus() {
    const id = document.getElementById("order-id-input").value;
    const statusResult = document.getElementById("status-result");
    if (id && id == orderId - 1) {
        statusResult.textContent = `Status for order ${id}: Pending`;
    } else {
        statusResult.textContent = `Incorrect Order ID`;
    }
}

loadProducts();
