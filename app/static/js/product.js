function addToCart(product) {
    // Отримуємо поточний кошик з localStorage
    let cart = JSON.parse(localStorage.getItem('cart')) || [];

    console.log("Додано до кошика:", product);

    // Перевіряємо, чи товар вже є у кошику
    const existingProduct = cart.find((item) => item.id === product.id);

    if (existingProduct) {
        // Якщо товар вже є у кошику, збільшуємо його кількість
        existingProduct.quantity += 1;
    } else {
        // Якщо товару немає у кошику, додаємо його
        product.quantity = 1; // Додаємо поле quantity (кількість)
        cart.push(product);
    }

    // Зберігаємо оновлений кошик у localStorage
    localStorage.setItem('cart', JSON.stringify(cart));

    // Повідомлення про успішне додавання
    alert(`Товар "${product.name}" додано до кошика!`);
}