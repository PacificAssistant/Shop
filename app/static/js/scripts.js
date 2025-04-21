document.addEventListener("DOMContentLoaded", function () {
    const themeButtons = document.querySelectorAll("[data-bs-theme-value]");

    themeButtons.forEach((button) => {
        button.addEventListener("click", () => {
            const theme = button.getAttribute("data-bs-theme-value");
            document.documentElement.setAttribute("data-bs-theme", theme);
            localStorage.setItem("theme", theme);

            // Оновлюємо активну кнопку
            themeButtons.forEach(btn => btn.classList.remove("active"));
            button.classList.add("active");
        });
    });

    // Відновлення теми при завантаженні сторінки
    const savedTheme = localStorage.getItem("theme") || "auto";
    document.documentElement.setAttribute("data-bs-theme", savedTheme);

    // Виділення активної теми в меню
    themeButtons.forEach(button => {
        if (button.getAttribute("data-bs-theme-value") === savedTheme) {
            button.classList.add("active");
        }
    });
});

document.addEventListener('hidden.bs.offcanvas', function () {
    document.body.style.overflow = 'auto';
});

// Оновлення даних при відкритті модального вікна
function addToCart(product) {
    let cart = JSON.parse(localStorage.getItem("cart")) || [];
    let existingProduct = cart.find(item => item.id === product.id);

    if (existingProduct) {
        existingProduct.quantity += 1;
    } else {
        product.quantity = 1;
        cart.push(product);
    }

    localStorage.setItem("cart", JSON.stringify(cart));

    alert(`${product.name} додано в кошик!`);
}

// Функція для показу повідомлення


document.addEventListener("DOMContentLoaded", function () {
    const cartModal = document.getElementById("cartModal");

    if (!cartModal) {
        console.error("❌ Елемент #cartModal не знайдено!");
        return;
    }

    cartModal.addEventListener("show.bs.modal", function () {
        const modalBody = document.querySelector("#cartModal .modal-body");

        if (!modalBody) {
            console.error("❌ Елемент .modal-body не знайдено!");
            return;
        }

        modalBody.innerHTML = "";  // Тепер помилка не виникне
        let cart = JSON.parse(localStorage.getItem("cart")) || [];

        if (cart.length === 0) {
            modalBody.innerHTML = "<p>Корзина порожня</p>";
            return;
        }

        const staticPath = "/static/";

        cart.forEach((product, index) => {
            const cartItem = document.createElement("div");
            cartItem.classList.add("cart-item", "d-flex", "align-items-center", "justify-content-between", "mb-2");

            cartItem.innerHTML = `
                <div class="d-flex align-items-center">
                    <img src="${staticPath}${product.image}" alt="${product.name}" class="cart-img" 
                        style="width: 50px; height: 50px; object-fit: cover; margin-right: 10px;">
                    <div>
                        <h6 class="mb-0">${product.name}</h6>
                        <p class="mb-0">Кількість: ${product.quantity}</p>
                    </div>
                </div>
                <button class="btn btn-danger btn-sm remove-item" data-index="${index}" 
                    style="margin-left: 10px;">&times;</button>
            `;

            modalBody.appendChild(cartItem);
        });

        // Додаємо кнопку "Оформити покупку"
        const checkoutButton = document.createElement("button");
        checkoutButton.textContent = "Оформити покупку";
        checkoutButton.classList.add("btn", "btn-success", "mt-3", "w-100");
        checkoutButton.addEventListener("click", function () {
            window.location.href = "/checkout";
        });

        modalBody.appendChild(checkoutButton);

        // Оновлюємо обробники для кнопок видалення товару
        document.querySelectorAll(".remove-item").forEach(button => {
            button.addEventListener("click", function () {
                const index = this.getAttribute("data-index");
                cart.splice(index, 1); // Видаляємо товар з масиву
                localStorage.setItem("cart", JSON.stringify(cart)); // Оновлюємо LocalStorage

                // Оновлюємо модальне вікно
                cartModal.dispatchEvent(new Event("show.bs.modal"));
            });
        });
    });
});


document.addEventListener("DOMContentLoaded", function () {
    let cart = JSON.parse(localStorage.getItem("cart")) || [];
    let cartItemsDiv = document.getElementById("cartItems");
    let totalPrice = 0;

    // Очищаємо блок перед додаванням товарів
    cartItemsDiv.innerHTML = "";

    if (cart.length === 0) {
        cartItemsDiv.innerHTML = "<p>Кошик порожній</p>";
        return;
    }

    cart.forEach(product => {
        let itemDiv = document.createElement("div");
        itemDiv.innerHTML = `<p>${product.name} x ${product.quantity} - ${product.price * product.quantity} грн</p>`;
        cartItemsDiv.appendChild(itemDiv);
        totalPrice += product.price * product.quantity;
    });

    document.getElementById("totalPrice").textContent = totalPrice;

    // Передаємо кошик у приховане поле перед відправкою форми
    document.getElementById("orderForm").addEventListener("submit", function () {
        document.getElementById("cartData").value = JSON.stringify(cart);
    });
});


