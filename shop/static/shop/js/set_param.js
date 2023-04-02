document.addEventListener("DOMContentLoaded", () => {
  const selectBtn = document.getElementById("select-btn");
  let colorSelect = document.querySelectorAll(".select-color");
  let sizeSelect = document.querySelectorAll(".select");
  const addInCartBtn = document.getElementById("add_in_cart");
  const selectOptions2 = document.getElementById("select-options-2");
  const productID = document.getElementById("product_id").textContent.trim();
  let priceProduct = document.getElementById("price_product").textContent;
  let nameProduct = document.getElementById("name_product").textContent;
  const selectBtns = document.querySelectorAll('.choce-param');
  const selectOptions = document.querySelectorAll('.params-product ul');
  const urlMainPhotoPr = document.getElementById("main_photo_product").textContent;
  let selectedSize = null;
  let selectedColor = null;

  // добавляем обработчик события для каждой кнопки
  selectBtns.forEach(function(btn, index) {
    btn.addEventListener('click', function() {
      if (selectOptions[index].style.display === 'block') {
        selectOptions[index].style.display = 'none';
      } else {
        selectOptions[index].style.display = 'block';
      }
    });
  });

  selectOptions.forEach(function(options) {
    options.addEventListener('click', function(e) {
      const selectedValue = e.target.getAttribute('data-value');
      const selectBtn = options.previousElementSibling;
      selectBtn.textContent = e.target.textContent;
      options.style.display = 'none';
      // Действия при выборе опции
      if (selectBtn.id === "select-btn") {
        selectedColor = e.target.textContent;
        console.log(selectedSize, selectedColor);
      } else if (selectBtn.id === "select-btn2") {
        selectedSize = e.target.textContent;
        console.log(selectedSize, selectedColor);
      }
    });
  });
  // Функция для очистки selectOptions2
  function clearOptions2() {
    selectOptions2.innerHTML = '<li data-value="" class="select"> Сначала выберите цвет </li>';
  }

  // Функция для заполнения selectOptions2 размерами
  async function fillOptions2(color) {
    try {
      const response = await fetch(`/api/size/?product_id=${productID}&color=${color}`);
      const sizes = await response.json();
      selectOptions2.innerHTML = sizes.map(size => `<li data-value="${size.size}">${size.size}</li>`).join("");
    } catch (error) {
      console.log(error);
      getDialogPopup("Сбой запроса по доступным размерам", "ОК");
    }
  }

  // Событие клика на кнопке selectBtn
  selectBtn.addEventListener("click", () => {
    selectOptions2.classList.toggle("active");
  });

  // Событие клика на цвет
  colorSelect.forEach(color => {
    color.addEventListener("click", () => {
      clearOptions2();
      selectedColor = color.getAttribute("data-value");
      fillOptions2(selectedColor);
      selectBtn.textContent = selectedColor;
    });
  });

  // Событие клика на размер
  sizeSelect.forEach(size => {
    size.addEventListener("click", () => {
      sizeSelect.forEach(size => size.classList.remove("selected"));
      size.classList.add("selected");
    });
  });

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

  addInCartBtn.addEventListener("click", () => {
  console.log(selectedSize, selectedColor);
  let product = {};
  if (!selectedSize || !selectedColor) {
    getDialogPopup("Пожалуйста сначала выберите цвет и размер", "Понятно");
    return;
  }
  selectedColor = selectedColor.trim();
  selectedSize = selectedSize.trim();

  async function getAmountProduct() {
    try {
      const response = await fetch(`/api/amount/?product_id=${productID}&color=${selectedColor}&size=${selectedSize}`);
      const data = await response.json();
      const listData = [];
      listData.push(data.amount);
      listData.push(data.pk);
      return listData;
    } catch (error) {
      console.log(error);
    }
  }

  getAmountProduct().then(async (amount) => {

    try {
      const arrayData = await getAmountProduct();

      console.log(arrayData[0], arrayData[1]);
      product = {
        id: productID,
        name: nameProduct,
        price: priceProduct,
        size: selectedSize,
        color: selectedColor,
        urlPhoto: urlMainPhotoPr,
        amount: arrayData[0],
        pk: arrayData[1],
        count_ord: 1
      };
      console.log(product);

      let cartProducts = localStorage.getItem("cartProducts");

      if (cartProducts && cartProducts.length > 0) {
        cartProducts = JSON.parse(cartProducts);

        for (let i = 0; i < cartProducts.length; i++) {
          if (cartProducts[i].id === productID && cartProducts[i].size === selectedSize && cartProducts[i].color === selectedColor) {
            getDialogPopup("Такой товар уже добавлен в корзину", "Закрыть");
            return;
          }
        }
        cartProducts.push(product);
      } else {
        cartProducts = [product];
      }

      localStorage.setItem("cartProducts", JSON.stringify(cartProducts));
      getDialogPopup("Товар добавлен в корзину", "OK");

    } catch (error) {
      console.log(error);
    }

  }).catch(error => {
    console.log(error);
  });
});

});


