document.addEventListener('DOMContentLoaded', function() {
    let slideIndex = 0;
    const slides = document.querySelectorAll('.slides');
    const prevArrow = document.querySelector('.prev-arrow');
    const nextArrow = document.querySelector('.next-arrow');

// функция для показа следующего слайда
    function showNextSlide() {
        slides[slideIndex].classList.remove('active');
        slideIndex = (slideIndex + 1) % slides.length;
        slides[slideIndex].classList.add('active');
    }

// функция для показа предыдущего слайда
    function showPrevSlide() {
        slides[slideIndex].classList.remove('active');
        slideIndex = (slideIndex - 1 + slides.length) % slides.length;
        slides[slideIndex].classList.add('active');
    }

// назначаем обработчики событий для стрелок
    prevArrow.addEventListener('click', showPrevSlide);
    nextArrow.addEventListener('click', showNextSlide);

// добавляем класс `active` первому слайду
    slides[slideIndex].classList.add('active');

});
