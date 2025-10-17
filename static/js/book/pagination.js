// Добавьте этот JavaScript для работы пагинатора
document.addEventListener('DOMContentLoaded', function() {
    const paginationLinks = document.querySelectorAll('.page-link:not(.dots)');
    const pageItems = document.querySelectorAll('.page-item');
    const currentItems = document.querySelector('.current-items');
    const totalItems = document.querySelector('.total-items');
    
    // Обработчик клика по страницам
    paginationLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            
            // Убираем активный класс у всех страниц
            pageItems.forEach(item => {
                item.classList.remove('active');
            });
            
            // Добавляем активный класс текущей странице
            if (!this.classList.contains('prev') && !this.classList.contains('next')) {
                this.parentElement.classList.add('active');
            }
            
            // Эффект нажатия
            this.style.transform = 'scale(0.95)';
            setTimeout(() => {
                this.style.transform = '';
            }, 150);
            
            // Здесь можно добавить логику загрузки новой страницы
            console.log('Переход на страницу:', this.textContent);
            
            // Обновляем информацию о странице (пример)
            updatePageInfo(this.textContent);
        });
    });
    
    // Функция обновления информации о странице
    function updatePageInfo(pageNumber) {
        const itemsPerPage = 8;
        const startItem = (pageNumber - 1) * itemsPerPage + 1;
        const endItem = pageNumber * itemsPerPage;
        
        if (currentItems) {
            currentItems.textContent = `${startItem}-${endItem}`;
        }
    }
    
    // Инициализация
    updatePageInfo(1);
});