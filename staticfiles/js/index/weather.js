// litnet-carousel-fixed.js
(function() {
    'use strict';
    
    class LitnetCarousel {
        constructor(container) {
            this.container = container;
            this.slides = [];
            this.indicators = [];
            this.currentIndex = 0;
            this.interval = null;
            this.slideDuration = 5000;
            this.isInitialized = false;
            
            this.init();
        }
        
        init() {
            if (!this.container) {
                console.error('Контейнер карусели не найден');
                return;
            }
            
            // Находим элементы внутри контейнера
            this.slides = Array.from(this.container.querySelectorAll('.litnet-carousel-slide'));
            this.indicators = Array.from(this.container.querySelectorAll('.litnet-indicator'));
            this.prevBtn = this.container.querySelector('.litnet-prev-btn');
            this.nextBtn = this.container.querySelector('.litnet-next-btn');
            this.progressBar = this.container.querySelector('.litnet-carousel-progress');
            
            if (this.slides.length === 0) {
                console.error('Слайды не найдены');
                return;
            }
            
            console.log('Найдено слайдов:', this.slides.length);
            console.log('Найдено индикаторов:', this.indicators.length);
            console.log('Кнопки:', {
                prev: !!this.prevBtn,
                next: !!this.nextBtn
            });
            
            this.bindEvents();
            this.showSlide(0);
            this.startAutoPlay();
            
            this.isInitialized = true;
            console.log('Карусель инициализирована');
        }
        
        bindEvents() {
            // Кнопка "назад"
            if (this.prevBtn) {
                this.prevBtn.addEventListener('click', () => {
                    this.stopAutoPlay();
                    this.prevSlide();
                    this.startAutoPlay();
                });
            }
            
            // Кнопка "вперед"
            if (this.nextBtn) {
                this.nextBtn.addEventListener('click', () => {
                    this.stopAutoPlay();
                    this.nextSlide();
                    this.startAutoPlay();
                });
            }
            
            // Индикаторы
            this.indicators.forEach((indicator, index) => {
                indicator.addEventListener('click', () => {
                    this.stopAutoPlay();
                    this.showSlide(index);
                    this.startAutoPlay();
                });
            });
            
            // Пауза при наведении
            this.container.addEventListener('mouseenter', () => this.stopAutoPlay());
            this.container.addEventListener('mouseleave', () => this.startAutoPlay());
            
            // Свайпы для мобильных
            this.setupTouchEvents();
        }
        
        setupTouchEvents() {
            let startX = 0;
            let endX = 0;
            
            this.container.addEventListener('touchstart', (e) => {
                startX = e.touches[0].clientX;
            });
            
            this.container.addEventListener('touchend', (e) => {
                endX = e.changedTouches[0].clientX;
                this.handleSwipe(startX, endX);
            });
        }
        
        handleSwipe(startX, endX) {
            const swipeThreshold = 50;
            
            if (startX - endX > swipeThreshold) {
                // Свайп влево
                this.stopAutoPlay();
                this.nextSlide();
                this.startAutoPlay();
            } else if (endX - startX > swipeThreshold) {
                // Свайп вправо
                this.stopAutoPlay();
                this.prevSlide();
                this.startAutoPlay();
            }
        }
        
        showSlide(index) {
            // Скрываем все слайды
            this.slides.forEach(slide => {
                slide.classList.remove('litnet-active');
            });
            
            // Убираем активность со всех индикаторов
            this.indicators.forEach(indicator => {
                indicator.classList.remove('litnet-active');
            });
            
            // Показываем нужный слайд
            this.currentIndex = (index + this.slides.length) % this.slides.length;
            this.slides[this.currentIndex].classList.add('litnet-active');
            
            // Активируем соответствующий индикатор
            if (this.indicators[this.currentIndex]) {
                this.indicators[this.currentIndex].classList.add('litnet-active');
            }
            
            this.resetProgressBar();
        }
        
        nextSlide() {
            this.showSlide(this.currentIndex + 1);
        }
        
        prevSlide() {
            this.showSlide(this.currentIndex - 1);
        }
        
        startAutoPlay() {
            this.stopAutoPlay();
            this.interval = setInterval(() => {
                this.nextSlide();
            }, this.slideDuration);
            
            this.resetProgressBar();
        }
        
        stopAutoPlay() {
            if (this.interval) {
                clearInterval(this.interval);
                this.interval = null;
            }
            if (this.progressBar) {
                this.progressBar.style.transition = 'none';
                this.progressBar.style.width = '0%';
            }
        }
        
        resetProgressBar() {
            if (!this.progressBar) return;
            
            // Сбрасываем анимацию
            this.progressBar.style.width = '0%';
            this.progressBar.style.transition = 'none';
            
            // Запускаем заново
            setTimeout(() => {
                this.progressBar.style.transition = `width ${this.slideDuration}ms linear`;
                this.progressBar.style.width = '100%';
            }, 10);
        }
        
        destroy() {
            this.stopAutoPlay();
            // Удаляем обработчики событий
            // (в реальном проекте нужно сохранять ссылки на обработчики)
        }
    }
    
    // Инициализация при загрузке DOM
    function initCarousels() {
        console.log('Поиск каруселей...');
        const carouselContainers = document.querySelectorAll('.litnet-carousel-container');
        
        console.log('Найдено контейнеров:', carouselContainers.length);
        
        if (carouselContainers.length === 0) {
            console.warn('Карусели не найдены на странице');
            return;
        }
        
        // Инициализируем каждую карусель
        window.litnetCarousels = [];
        carouselContainers.forEach((container, index) => {
            console.log(`Инициализация карусели ${index + 1}`);
            const carousel = new LitnetCarousel(container);
            window.litnetCarousels.push(carousel);
        });
        
        console.log('Все карусели инициализированы');
    }
    
    // Запускаем инициализацию когда DOM готов
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initCarousels);
    } else {
        initCarousels();
    }
    
    // Экспортируем для глобального доступа
    window.LitnetCarousel = LitnetCarousel;
})();