//Add star rating
const rating = document.querySelector('form[name=rating]');

rating.addEventListener("change", function (e) {
    // Получаем данные из формы
    let data = new FormData(this);
    fetch(`${this.action}`, {
        method: 'POST',
        body: data
    })
        .then(response => alert("Рейтинг установлен"))
        .catch(error => alert("Ошибка"))
});


//static star //

"use strict"
const ratings = document.querySelectorAll('.ratingg');
if (ratings.length > 0) {
    initRatings();
}

// base fun
function initRatings() {
    let ratingActive, ratingValue;
    for (let index = 0; index < ratings.length; index++) {
        const rating = ratings[index];
        initRating(rating);
    }

    function initRating(rating) {
        initRatingVars(rating);

        setRatingActiveWidth();
    }
    function initRatingVars(rating) {
        ratingActive = rating.querySelector('.rating__activee');
        ratingValue = rating.querySelector('.rating__valuee');
    }

    function setRatingActiveWidth(index = ratingValue.innerHTML) {
        const ratingActiveWidth = index / 0.05;
        ratingActive.style.width = `${ratingActiveWidth}%`;
    }
}



















