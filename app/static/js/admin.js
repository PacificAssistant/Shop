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