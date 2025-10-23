document.addEventListener('DOMContentLoaded', function() {
    // Элементы DOM
    const bookPage = document.getElementById('bookPage');
    const prevPageBtn = document.getElementById('prevPage');
    const nextPageBtn = document.getElementById('nextPage');
    const currentPageSpan = document.querySelector('.current-page');
    const progressFill = document.querySelector('.progress-fill');
    const progressText = document.querySelector('.reading-progress span');
    
    // Настройки шрифта
    const fontSizeDown = document.getElementById('fontSizeDown');
    const fontSizeNormal = document.getElementById('fontSizeNormal');
    const fontSizeUp = document.getElementById('fontSizeUp');
    
    // Переменные состояния
    let currentPage = 1;
    const totalPages = 384;
    let fontSize = 1; // множитель размера шрифта
    let isNightMode = false;

    // Анимация перелистывания страницы
    function flipPage(direction) {
        bookPage.style.transform = 'rotateY(90deg)';
        bookPage.style.opacity = '0';
        
        setTimeout(() => {
            
            bookPage.style.transform = 'rotateY(0deg)';
            bookPage.style.opacity = '1';
        }, 300);
    }


    // Управление размером шрифта
    function setFontSize(size) {
        fontSize = size;
        const pageContent = document.querySelector('.page-content');
        
        if (size === 0.9) {
            pageContent.style.fontSize = '0.9rem';
            fontSizeDown.classList.add('active');
            fontSizeNormal.classList.remove('active');
            fontSizeUp.classList.remove('active');
        } else if (size === 1) {
            pageContent.style.fontSize = '1rem';
            fontSizeDown.classList.remove('active');
            fontSizeNormal.classList.add('active');
            fontSizeUp.classList.remove('active');
        } else if (size === 1.1) {
            pageContent.style.fontSize = '1.1rem';
            fontSizeDown.classList.remove('active');
            fontSizeNormal.classList.remove('active');
            fontSizeUp.classList.add('active');
        }
    }

    // Переключение ночного режима
    function toggleNightMode() {
        isNightMode = !isNightMode;
        const container = document.querySelector('.book-reader-container');
        const toggleBtn = document.getElementById('toggleTheme');
        
        if (isNightMode) {
            container.classList.add('night-mode');
            toggleBtn.innerHTML = '<span>☀️</span> Дневной режим';
        } else {
            container.classList.remove('night-mode');
            toggleBtn.innerHTML = '<span>🌙</span> Ночной режим';
        }
    }

    // Эффект добавления закладки
    function addBookmark() {
        const bookmarkBtn = document.getElementById('bookmarkBtn');
        bookmarkBtn.innerHTML = '<span>✅</span> Закладка добавлена!';
        bookmarkBtn.style.background = 'linear-gradient(135deg, #48bb78 0%, #38a169 100%)';
        
        // Создаем эффект "всплывающего уведомления"
        const notification = document.createElement('div');
        notification.className = 'bookmark-notification';
        notification.textContent = `Закладка на странице ${currentPage} добавлена!`;
        document.querySelector('.reader-settings').appendChild(notification);
        
        setTimeout(() => {
            notification.classList.add('show');
        }, 10);
        
        setTimeout(() => {
            notification.classList.remove('show');
            setTimeout(() => {
                notification.remove();
                bookmarkBtn.innerHTML = '<span>🔖</span> Закладка';
                bookmarkBtn.style.background = '';
            }, 300);
        }, 2000);
    }

    // Подсветка текста при выделении
    function enableTextHighlight() {
        const pageContent = document.querySelector('.page-content');
        
        pageContent.addEventListener('mouseup', function() {
            const selection = window.getSelection();
            if (selection.toString().length > 0) {
                // Создаем кнопку для выделения
                const highlightBtn = document.createElement('button');
                highlightBtn.className = 'highlight-btn';
                highlightBtn.innerHTML = '★ Выделить';
                highlightBtn.style.position = 'absolute';
                highlightBtn.style.left = `${selection.getRangeAt(0).getBoundingClientRect().left}px`;
                highlightBtn.style.top = `${selection.getRangeAt(0).getBoundingClientRect().top - 40}px`;
                
                highlightBtn.addEventListener('click', function() {
                    const range = selection.getRangeAt(0);
                    const highlight = document.createElement('span');
                    highlight.className = 'text-highlighted';
                    highlight.style.backgroundColor = 'rgba(255, 235, 59, 0.3)';
                    range.surroundContents(highlight);
                    highlightBtn.remove();
                    selection.removeAllRanges();
                });
                
                document.querySelector('.page-container').appendChild(highlightBtn);
                
                // Убираем кнопку при клике вне ее
                setTimeout(() => {
                    document.addEventListener('click', function removeBtn(e) {
                        if (!highlightBtn.contains(e.target)) {
                            highlightBtn.remove();
                            document.removeEventListener('click', removeBtn);
                        }
                    });
                }, 100);
            }
        });
    }

    // Навигация с клавиатуры
    function enableKeyboardNavigation() {
        document.addEventListener('keydown', function(e) {
            if (e.key === 'ArrowLeft') {
                flipPage('prev');
            } else if (e.key === 'ArrowRight') {
                flipPage('next');
            } else if (e.key === 'n' || e.key === 'N') {
                toggleNightMode();
            }
        });
    }

    // Инициализация событий
    prevPageBtn.addEventListener('click', () => flipPage('prev'));
    nextPageBtn.addEventListener('click', () => flipPage('next'));
    
    fontSizeDown.addEventListener('click', () => setFontSize(0.9));
    fontSizeNormal.addEventListener('click', () => setFontSize(1));
    fontSizeUp.addEventListener('click', () => setFontSize(1.1));
    
    document.getElementById('toggleTheme').addEventListener('click', toggleNightMode);
    document.getElementById('bookmarkBtn').addEventListener('click', addBookmark);
    
    // Инициализация функций
    enableTextHighlight();
    enableKeyboardNavigation();
    
    // Параллакс эффект для фона при скролле
    window.addEventListener('scroll', function() {
        const scrolled = window.pageYOffset;
        const parallax = document.querySelector('.book-reader-container');
        parallax.style.backgroundPosition = `center ${scrolled * 0.5}px`;
    });
});