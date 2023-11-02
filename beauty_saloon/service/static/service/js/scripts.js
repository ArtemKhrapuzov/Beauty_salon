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

//const rating = document.querySelector('form[name=rating]');
//const stars = document.querySelectorAll('.rating input[type=radio]');
//
//rating.addEventListener("change", function (e) {
//    // Получаем данные из формы
//    let data = new FormData(this);
//    fetch(${this.action}, {
//        method: 'POST',
//        body: data
//    })
//        .then(response => {
//            alert("Рейтинг установлен");
//            // Обновляем количество звезд
//            const averageRating = document.querySelector('.editContent').textContent;
//            const fullStars = Math.floor(averageRating);
//            const halfStar = (averageRating - fullStars) >= 0.5 ? 1 : 0;
//            for (let i = 0; i < fullStars; i++) {
//                stars[i].classList.add('active');
//            }
//            if (halfStar) {
//                stars[fullStars].classList.add('half');
//            }
//        })
//        .catch(error => alert("Ошибка"))
//});