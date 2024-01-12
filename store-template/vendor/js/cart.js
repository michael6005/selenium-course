let cartItems = [];

function addToCart() {
    // Находим родительский элемент кнопки "Добавить в корзину", чтобы получить доступ к данным товара
    const productCard = event.target.parentNode.parentNode;
    const productTitle = productCard.querySelector("h4").innerText;
    const productPrice = productCard.querySelector("h5").innerText;
    const productDescription = productCard.querySelector("p").innerText;

    // Создаем объект товара и добавляем его в массив корзины
    const product = {
        title: productTitle,
        description: productDescription,
        price: productPrice,
    };
    cartItems.push(product);

    // Сохраняем выбранные товары в LocalStorage
    localStorage.setItem("cartItems", JSON.stringify(cartItems));

    console.log(cartItems);
}

function renderCartItems() {
    const storedCartItems = localStorage.getItem("cartItems");
    if (storedCartItems) {
        const cartItems = JSON.parse(storedCartItems);

        const card = document.querySelector(".card-body");
        const cardFooter = document.querySelector(".card-footer");

        cartItems.forEach(function (item) {
            const cardTitle = card.querySelector('.card-title');
            cardTitle.textContent = item['title'];

            const cardDescription = card.querySelector('.card-text');
            cardDescription.textContent = item['description'];

            const cardPrice = cardFooter.querySelector('#card-price');
            cardPrice.textContent = item['price'];
        })
    }
    localStorage.clear();
}

function clearCart() {
    // Удаляем все товары из localStorage
    localStorage.clear();

    // Получаем элемент списка товаров
    const cartItemsList = document.getElementById("cart");

    // Создаем новый элемент с надписью "Нет добавленных товаров"
    const emptyMessage = document.createElement("h3");
    emptyMessage.textContent = "Нет добавленных товаров";

    // Скрываем список товаров и добавляем новый элемент на страницу
    cartItemsList.style.display = "none";
    cartItemsList.parentNode.insertBefore(emptyMessage, cartItemsList);
}