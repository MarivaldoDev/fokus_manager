// Controla o comportamento do menu mobile
document.addEventListener('DOMContentLoaded', function() {
    const navbarToggler = document.querySelector('.navbar-toggler');
    const navbarCollapse = document.querySelector('.navbar-collapse');
    const body = document.body;

    if (navbarToggler && navbarCollapse) {
        // Adiciona classe ao body quando menu abre
        navbarToggler.addEventListener('click', function() {
            if (navbarCollapse.classList.contains('show')) {
                body.classList.add('navbar-open');
            } else {
                body.classList.remove('navbar-open');
            }
        });

        // Remove classe quando clica em um link
        const navLinks = navbarCollapse.querySelectorAll('.nav-link, .btn');
        navLinks.forEach(link => {
            link.addEventListener('click', function() {
                // Pequeno delay para não quebrar a animação
                setTimeout(() => {
                    navbarToggler.click();
                }, 100);
            });
        });

        // Fecha o menu quando clica no backdrop
        body.addEventListener('click', function(e) {
            if (e.target === body && navbarCollapse.classList.contains('show')) {
                navbarToggler.click();
            }
        });
    }
});
