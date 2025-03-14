document.addEventListener("DOMContentLoaded", function () {
    const themeButtons = document.querySelectorAll("[data-bs-theme-value]");

    function setTheme(theme) {
        document.documentElement.setAttribute("data-bs-theme", theme);
        localStorage.setItem("theme", theme);
    }

    // Завантаження збереженої теми
    const savedTheme = localStorage.getItem("theme") || "auto";
    setTheme(savedTheme);

    themeButtons.forEach((button) => {
        button.addEventListener("click", function () {
            const selectedTheme = this.getAttribute("data-bs-theme-value");
            setTheme(selectedTheme);

            // Позначення активної кнопки
            themeButtons.forEach(btn => {
                btn.classList.remove("active");
                btn.setAttribute("aria-pressed", "false");
            });

            this.classList.add("active");
            this.setAttribute("aria-pressed", "true");
        });
    });
});
