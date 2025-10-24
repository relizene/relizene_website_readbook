// Простой JavaScript для мобильного меню (если Bootstrap не работает)
document.addEventListener('DOMContentLoaded', function() {
    const mobileMenuBtn = document.querySelector('.mobile-menu-btn');
    const mobileNavbar = document.getElementById('mobileNavbar');
    const closeMobileMenu = document.querySelector('.close-mobile-menu');
    
    // Функция открытия/закрытия меню
    function toggleMobileMenu() {
        if (mobileNavbar.classList.contains('show')) {
            closeMobileMenu();
        } else {
            openMobileMenu();
        }
    }
    
    function openMobileMenu() {
        mobileNavbar.classList.add('show');
        document.body.classList.add('menu-open');
        // Обновляем aria-атрибуты
        mobileMenuBtn.setAttribute('aria-expanded', 'true');
        mobileNavbar.setAttribute('aria-hidden', 'false');
    }
    
    function closeMobileMenu() {
        mobileNavbar.classList.remove('show');
        document.body.classList.remove('menu-open');
        // Обновляем aria-атрибуты
        mobileMenuBtn.setAttribute('aria-expanded', 'false');
        mobileNavbar.setAttribute('aria-hidden', 'true');
    }
    
    // Обработчики событий
    if (mobileMenuBtn) {
        mobileMenuBtn.addEventListener('click', toggleMobileMenu);
    }
    
    if (closeMobileMenu) {
        closeMobileMenu.addEventListener('click', closeMobileMenu);
    }
    
    // Закрытие меню при клике на ссылку
    const mobileNavLinks = document.querySelectorAll('.mobile-nav-link');
    mobileNavLinks.forEach(link => {
        link.addEventListener('click', closeMobileMenu);
    });
    
    // Закрытие меню при клике вне меню
    document.addEventListener('click', function(e) {
        if (mobileNavbar.classList.contains('show') && 
            !mobileNavbar.contains(e.target) && 
            !mobileMenuBtn.contains(e.target)) {
            closeMobileMenu();
        }
    });
    
    // Закрытие меню при нажатии Escape
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && mobileNavbar.classList.contains('show')) {
            closeMobileMenu();
        }
    });
});