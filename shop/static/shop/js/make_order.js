document.addEventListener('DOMContentLoaded', function() {
  const makeOrderBtn = document.querySelector('#make_order');
  let order = null;

  makeOrderBtn.addEventListener('click', async (event) => {
    //event.preventDefault();
    // Получаем данные из HTML формы
    const description = document.querySelector('#description').value;
    const address = document.querySelector('#address').value;
    const paymentMethod = document.querySelector('#payment_method').value;
    const token = sessionStorage.getItem('token');

    //const sessionid =
    // document.cookie.match('(^|;)\\s*sessionid\\s*=\\s*([^;]+)')?.pop() || '';
    if(!token){
      getDialogPopup('Время действия вашего токена истекло. Пожалуйста,' +
          ' заново авторизуйтесь на сайте', 'ОК');
      return;
    }
    console.log(token);
    console.log(description)
    console.log(address)
    console.log(paymentMethod)
    // console.log(sessionid)
    if (!description || !address || !paymentMethod) {
      getDialogPopup('Пожалуйста, заполните все поля формы', 'ОК');
      return;
    }

    // Отправляем запрос на создание экземпляра модели Order

    try {
      const orderResponse = await fetch('/api/orders/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Token ' + token
        },
        body: JSON.stringify({
          "description": description,
          "adress": address,
          "payment_method": paymentMethod,
        }),
      });
      order = await orderResponse.json();
    } catch (error) {
      console.error('Error:', error);
    }

    // Получаем данные из localStorage
    const cartProducts = JSON.parse(localStorage.getItem('cartProducts'));
    if (order !== null) {
      // Отправляем запросы на создание экземпляров модели OrderProduct и связей с моделями Order и Product
      for (let i = 0; i < cartProducts.length; i++) {
        const cartItem = cartProducts[i];
        const pkProduct = cartItem.pk;
        const count = cartItem.count_ord;
        console.log('pkProduct: ' + pkProduct);
        console.log(typeof(pkProduct));
        console.log('amount: ' + count);
        console.log(typeof(count));
        console.log('order.id: ' + order.id);
        console.log(typeof(order.id));

        try {
          const ProdOrdResponse = await fetch('/api/order_products/', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              'Authorization': 'Token ' + token
            },
            body: JSON.stringify({
              "count": count,
              "order": order.id,
              "product": pkProduct,
            }),
          });
          const result = await ProdOrdResponse.json();
          console.log(result);
        } catch (error) {
          console.error('Error:', error);
        }

      }
      const textMessage = 'Ваш заказ успешно создан, номер заказа ' + order.id;
      getDialogPopup(textMessage, 'ОК');
    } else {
      getDialogPopup('У вас нет созданных заказов, повторите или свяжитесь с' +
          ' разработчиком', 'ОК');
      return;
    }

    function getDialogPopup(message, text_btn) {
    let popupHtml = `
      <div class="popup-dialog">
        <div class="popup-dialog-content">
          <h2>${message}</h2>
          <button class="ok-btn">${text_btn}</button>
        </div>
      </div>`;
    document.documentElement.insertAdjacentHTML("beforeend", popupHtml);

    let okBtn = document.querySelector(".popup-dialog .ok-btn");
    let popupDialog = document.querySelector('.popup-dialog');

    function closePopup() {
      document.querySelector(".popup-dialog").remove();
      window.removeEventListener("click", outsideClickListener);
    }

    function outsideClickListener(event) {
      if (event.target == popupDialog) {
        closePopup();
      }
    }

    window.addEventListener("click", outsideClickListener);
    okBtn.addEventListener("click", closePopup);
  }

    // Удаляем данные из localStorage
    localStorage.removeItem('cartProducts');

    // // Перенаправляем пользователя на страницу заказов
    // window.location.href = '/shop/';
  });

});


