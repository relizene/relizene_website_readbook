 document.addEventListener('DOMContentLoaded', function() {
            // Анимация лайка
            const likeButton = document.getElementById('likeButton');
            const likeCount = document.getElementById('likeCount');
            let likes = parseInt(likeCount.textContent);
            let isLiked = false;

            likeButton.addEventListener('click', function() {
                if (!isLiked) {
                    likes++;
                    likeCount.textContent = likes;
                    likeButton.classList.add('liked');
                    
                    // Создаем эффект "пульсации"
                    likeButton.style.transform = 'scale(1.1)';
                    setTimeout(() => {
                        likeButton.style.transform = 'scale(1)';
                    }, 150);
                    
                    isLiked = true;
                } else {
                    likes--;
                    likeCount.textContent = likes;
                    likeButton.classList.remove('liked');
                    isLiked = false;
                }
            });

            // Параллакс эффект для плавающих форм
            const shapes = document.querySelectorAll('.shape');
            document.addEventListener('mousemove', (e) => {
                const mouseX = e.clientX / window.innerWidth;
                const mouseY = e.clientY / window.innerHeight;
                
                shapes.forEach((shape, index) => {
                    const speed = (index + 1) * 0.5;
                    const x = (mouseX * speed * 20) - 10;
                    const y = (mouseY * speed * 20) - 10;
                    
                    shape.style.transform = `translate(${x}px, ${y}px)`;
                });
            });

            // Плавное появление элементов при скролле
            const observerOptions = {
                threshold: 0.1,
                rootMargin: '0px 0px -50px 0px'
            };

            const observer = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        entry.target.style.opacity = '1';
                        entry.target.style.transform = 'translateY(0)';
                    }
                });
            }, observerOptions);

            // Наблюдаем за элементами с анимацией
            const animatedElements = document.querySelectorAll('.book-meta, .book-description, .stats-container');
            animatedElements.forEach(el => {
                el.style.opacity = '0';
                el.style.transform = 'translateY(20px)';
                el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
                observer.observe(el);
            });

            // Добавляем интерактивность к обложке
            const bookCover = document.querySelector('.book-cover');
            bookCover.addEventListener('mouseenter', () => {
                bookCover.style.transform = 'scale(1.05) rotateZ(1deg)';
            });
            
            bookCover.addEventListener('mouseleave', () => {
                bookCover.style.transform = 'scale(1) rotateZ(0deg)';
            });
        });