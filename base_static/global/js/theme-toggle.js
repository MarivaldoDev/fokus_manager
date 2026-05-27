document.addEventListener("DOMContentLoaded", function() {
    const themeBtn = document.getElementById("themeToggleBtn");
    const themeIcon = document.getElementById("themeIcon");
    const themeText = document.getElementById("themeText");
    
    function updateIcon(theme) {
        if (theme === 'dark') {
            themeIcon.classList.remove('bi-moon-stars-fill');
            themeIcon.classList.add('bi-sun-fill');
            themeIcon.classList.add('text-warning');
            themeText.textContent = "Modo Claro";
        } else {
            themeIcon.classList.remove('bi-sun-fill');
            themeIcon.classList.remove('text-warning');
            themeIcon.classList.add('bi-moon-stars-fill');
            themeText.textContent = "Modo Escuro";
        }
    }

    const currentTheme = document.documentElement.getAttribute("data-bs-theme") || "light";
    updateIcon(currentTheme);

    themeBtn.addEventListener("click", function() {
        let newTheme = document.documentElement.getAttribute("data-bs-theme") === "dark" ? "light" : "dark";
        
        document.documentElement.dataset.theme = newTheme;
        document.documentElement.setAttribute("data-bs-theme", newTheme);
        localStorage.setItem("theme", newTheme);
        
        updateIcon(newTheme);
    });
});
