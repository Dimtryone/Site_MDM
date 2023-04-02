document.addEventListener("DOMContentLoaded", function(event) {
  // Весь код скрипта помещаем здесь

  var openModalBtn = document.getElementById("open-modal-btn");
  var closeModalBtn = document.getElementById("close-modal-btn");
  var modal = document.getElementById("modal");

  openModalBtn.addEventListener("click", function () {
    modal.style.display = "block";
    updateOpenModal();
  });

  closeModalBtn.addEventListener("click", function () {
    modal.style.display = "none";
  });

  window.addEventListener("click", function (event) {
    if (event.target == modal) {
      modal.style.display = "none";

    }
  });

  function updateOpenModal() {
    let cartProducts = JSON.parse(localStorage.getItem("cartProducts"));
    if (!cartProducts){
      let ErrorCart = document.querySelector(".cart");
      ErrorCart.innerHTML = `
        <h2>Ваша корзина корзина пуста, пожалуйста выберите товар</h2>
      `;
    }
    let cartItemsHtml = "";
    for (let i = 0; i < cartProducts.length; i++) {
      let cartItem = cartProducts[i];
      let priceString = cartItem.price;
      let price = parseFloat(priceString.replace(/[^\d.,]/g, '').replace(',', '.'));
      cartItemsHtml += `
        <div class="cart-item">
          <div>
            <img src=${cartItem.urlPhoto} width="150" style="min-width: 150px" alt="This is photo of product">
            <div class="cart-inform">Остаток на складе: ${cartItem.amount}</div>
            <div class="disp_none">${cartItem.pk}</div>
          </div>
          <div class="cart-table">
 
            <table>
              <tr>
                <td>Наименование</td>
                <td>Размер</td>
                <td>Цвет</td>
                <td>Количество</td>
                <td>Цена</td>
                <td>Всего</td>                
              </tr>
              <tr>
                <td>${cartItem.name}</td>
                <td>${cartItem.size}</td>
                <td>${cartItem.color}</td>
                <td><div class="amount-view" id="${cartItem.pk}">
                      <div class="less">< </div>
                      <div>${cartItem.count_ord}</div>
                      <div class="more"> ></div>
                      <div class="disp_none">${cartItem.amount}</div>
                    </div>
                </td>
                <td class="price_tb">${price}</td>
                <td class="total_tb">${price}</td>
              </tr>
              <tr>
                <td></td>
                <td></td>
                <td></td>
                <td></td>
                <td></td>
                <td><button class="remove-from-cart" data-key="${i}">Удалить</button></td>
              </tr>             
            </table>
          </div>
        </div>`;
    }


    // добавляем разметку в модальное окно
    let modalContent = document.querySelector(".cart");
    if (modalContent) {
      modalContent.innerHTML = `
        <h3>Ваша корзина</h3>
        <div class="cart-items">${cartItemsHtml}</div>
        <div class="total">
          <h4>Сумма заказа:</h4>
          <h4 id="total_sum"></h4>
          <h4>руб.</h4>
        </div>
        <div class="submit_order_btn">
         <a href="${make_order_url}" class="make-order" id="make_order_btn_cart">Оформить заказ</a>
        </div>
      `;

       // // Находим все элементы с классами "less" и "more"
    let lessElements = document.querySelectorAll(".less");
    let moreElements = document.querySelectorAll(".more");

    // Добавляем обработчики событий на найденные элементы
    for (let i = 0; i < lessElements.length; i++) {
      lessElements[i].addEventListener("click", function() {
        let amountElement = this.nextElementSibling;
        let currentValue = parseInt(this.nextElementSibling.textContent.trim());
        let amountView = this.closest('.amount-view');
        let priceElement = amountView.closest('tr').querySelector('td:nth-child(5)');
        let totalElement = amountView.closest('tr').querySelector('td:nth-child(6)');
        const Price = parseFloat(priceElement.textContent);
        if (currentValue > 1) {
          amountElement.textContent = currentValue - 1;
          totalElement.textContent = (Price * (currentValue - 1)).toFixed(2);
          updateTotalSum();
        }
      });
    }

    for (let i = 0; i < moreElements.length; i++) {
      moreElements[i].addEventListener("click", function() {
        let amountElement = this.previousElementSibling;;
        let currentValue = parseInt(amountElement.textContent.trim());
        let maxAmount = parseInt(this.nextElementSibling.textContent);
        let amountView = this.closest('.amount-view');
        let priceElement = amountView.closest('tr').querySelector('td:nth-child(5)');
        let totalElement = amountView.closest('tr').querySelector('td:nth-child(6)');
        const Price = parseFloat(priceElement.textContent);
        if (currentValue < maxAmount) {
          amountElement.textContent = currentValue + 1;
          totalElement.textContent = (Price * (currentValue + 1)).toFixed(2);
          updateTotalSum();
        }
       });

      function updateTotalSum() {
        const totalElements = document.querySelectorAll('.total_tb');
        let totalSum = 0;

        totalElements.forEach((totalElement) => {
          totalSum += parseFloat(totalElement.textContent);
        });

        document.querySelector('#total_sum').textContent = totalSum.toFixed(2);
      }
      updateTotalSum();
    }
    }

    // добавляем обработчики событий для кнопок "Удалить"
    let removeButtons = modalContent.querySelectorAll(".remove-from-cart");
    for (let i = 0; i < removeButtons.length; i++) {
      removeButtons[i].addEventListener("click", function () {
        let key = parseInt(this.dataset.key);
        let cartProducts = JSON.parse(localStorage.getItem("cartProducts"));
        cartProducts.splice(key, 1);
        localStorage.setItem("cartProducts", JSON.stringify(cartProducts));
        updateOpenModal();
      });
    }

    const makeOrderBtn = document.getElementById("make_order_btn_cart")
    console.log(makeOrderBtn)
    makeOrderBtn.addEventListener("click", function(event){
      //event.preventDefault(); - использовал для отладки
      let cartProducts = JSON.parse(localStorage.getItem("cartProducts"));
      for (let i = 0; i < cartProducts.length; i++) {
        product = cartProducts[i];
        let id = String(product.pk);
        let element = document.getElementById(id);
        let count = parseInt(element.querySelector('div:nth-child(2)').textContent.trim());
        console.log(count);
        product.count_ord = count;
      }
      localStorage.setItem("cartProducts", JSON.stringify(cartProducts));
    });
  }
});




