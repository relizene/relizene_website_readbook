 // Дополнительная анимация при клике на карточку
        document.addEventListener('DOMContentLoaded', function() {
            const bookCards = document.querySelectorAll('.book-card');
            
            bookCards.forEach(card => {
                card.addEventListener('click', function() {
                    // Добавляем эффект "пульсации" при клике
                    this.style.transform = 'scale(0.95)';
                    setTimeout(() => {
                        this.style.transform = '';
                    }, 150);
                    
                    // Здесь можно добавить переход на страницу книги
                    console.log('Переход на страницу книги');
                });
            });
        });