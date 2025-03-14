// document.addEventListener("DOMContentLoaded", function () {
//     console.log("DOM повністю завантажений!");
//
//     let button = document.getElementById("generateButton");
//     if (button) {
//         button.addEventListener("click", generateProducts);
//     } else {
//         console.error("❌ Кнопка generateButton не знайдена!");
//     }
// });

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
// document.addEventListener("DOMContentLoaded", function () {
//     const productCountInput = document.getElementById("productCount");
//     const productGrid = document.getElementById("productGrid");
//     const generateButton = document.getElementById("generateButton");
//
//     // Оновлюємо поле вводу при зміні кількості товарів
//     productCountInput.value = products.length;
//
//     generateButton.addEventListener("click", function () {
//         const count = parseInt(productCountInput.value);
//         productGrid.innerHTML = ""; // Очищаємо grid перед оновленням
//
//         for (let i = 0; i < count; i++) {
//             const productData = products[i % products.length]; // Отримуємо товар
//             const product = document.createElement("div");
//             product.classList.add("product");
//
//             product.innerHTML = `
//                 <img src="${productData.image}" alt="Product">
//                 <p>${productData.name}</p>
//             `;
//             productGrid.appendChild(product);
//         }
//     });
// });


document.addEventListener('hidden.bs.offcanvas', function () {
    document.body.style.overflow = 'auto';
});
document.addEventListener("DOMContentLoaded", function () {
        const productCountInput = document.getElementById("productCount");
        const productGrid = document.getElementById("productGrid");

        // Встановлюємо кількість товарів у полі вводу
        productCountInput.value = productGrid.children.length;
    });
