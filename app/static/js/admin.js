document.getElementById("category-form").addEventListener("submit", function (event) {
    event.preventDefault();
    let categoryName = document.getElementById("category-name").value;

    fetch("{{ url_for('admin.add_category') }}", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({name: categoryName})
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                let select = document.getElementById("category-select");
                let option = document.createElement("option");
                option.value = data.category_id;
                option.textContent = categoryName;
                select.appendChild(option);
                alert("Категорія додана!");
            }
        });
});
document.getElementById("productSelect").addEventListener("change", function () {
    let productId = this.value;
    fetch(`/admin/get_product/${productId}`)
        .then(response => response.json())
        .then(data => {
            document.getElementById("name").value = data.name;
            document.getElementById("price").value = data.price;
            document.getElementById("stock").value = data.stock;
            document.getElementById("description").value = data.description;
        });
});

function updateProduct() {
    let formData = new FormData(document.getElementById("editProductForm"));
    fetch("/admin/update_product", {
        method: "POST",
        body: formData
    })
        .then(response => response.json())
        .then(data => alert(data.message))
        .catch(error => alert("Помилка оновлення"));
}