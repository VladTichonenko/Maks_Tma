// Добавляем класс 'loaded' к body для начальной загрузки
window.addEventListener('load', () => {
    document.body.classList.add('loaded');
    showFirstCard(); // Сразу показываем первую карточку
});

// Функция для показа первой карточки
function showFirstCard() {
    const firstCard = document.querySelector('.card-1');
    firstCard.classList.add('active');
}

// Функция для показа второй карточки
function showSecondCard() {
    const firstCard = document.querySelector('.card-1');
    const secondCard = document.querySelector('.card-2');
    
    // Скрываем первую карточку и показываем вторую
    firstCard.classList.remove('active');
    secondCard.classList.add('active');
}

// Функция для показа третьей карточки
function showThirdCard() {
    const secondCard = document.querySelector('.card-2');
    const thirdCard = document.querySelector('.card-3');

    // Скрываем вторую карточку и показываем третью
    secondCard.classList.remove('active');
    thirdCard.classList.add('active');
}

// Функция для перехода к темному экрану и увеличению изображения
function startTransition() {
    const centerImage = document.querySelector('.center-image img');
    const darkScreen = document.createElement('div');
    darkScreen.classList.add('dark-screen');
    document.body.appendChild(darkScreen);

    // Увеличиваем изображение
    centerImage.style.transform = 'scale(1.5)'; // Увеличиваем изображение

    // Ждем 0.8 секунды, затем показываем темный экран
    setTimeout(() => {
        darkScreen.style.opacity = '1'; // Делаем темный экран видимым

        // Через 3 секунды переходим на main.html
        setTimeout(() => {
            window.location.href = 'main.html';
        }, 3000);
    }, 800); // Увеличение изображения
}

// Функция для скрытия всех карточек
function hideCards() {
    const activeCards = document.querySelectorAll('.card.active');
    
    activeCards.forEach(card => {
        card.classList.remove('active');
    });
}
