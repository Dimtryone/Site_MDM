document.addEventListener("DOMContentLoaded", function(event) {
    // Весь код скрипта помещаем здесь

    var openModalBtn2 = document.getElementById("open-modal-btn2");
    var closeModalBtn2 = document.getElementById("close-modal-btn2");
    var modal = document.getElementById("modal2");

    openModalBtn2.addEventListener("click", function () {
        modal.style.display = "block";
        updateOpenModal2();
    });

    closeModalBtn2.addEventListener("click", function () {
        modal.style.display = "none";
    });

    window.addEventListener("click", function (event) {
        if (event.target == modal) {
            modal.style.display = "none";

        }
    });

  async function updateOpenModal2() {
    const token = sessionStorage.getItem('token');
    let data = [];
    let cartItemsHtml = "";
    let modalContent = document.querySelector("#cart2");

    try {
      const response = await fetch("/api/getstatus/", {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Token ' + token
        }
      });
      data = await response.json();
      for (let i = 0; i < data.length; i++) {
        let order = data[i];
        let nameStatus = order.status;
        let idOrder = order.id;
        let client = order.first_name;
        let num = i + 1
        cartItemsHtml += `
                <tr>
                  <td>${num}</td>
                  <td>${nameStatus}</td>
                  <td>${idOrder}</td>
                  <td>${client}</td>
                </tr>  
             `;
            }
      modalContent.innerHTML = `
      <h3>Список ваших заказов</h3>
      <div class="cart-items">
          <div class="cart-item">
            <div class="cart-table">
              <table>
                <tr>
                  <td>№</td>
                  <td>Статус</td>
                  <td>Номер заказа</td>   
                  <td>Имя заказчика</td>              
                </tr>
                ${cartItemsHtml}
                      
              </table>
            </div>
          </div>
        </div>`;

    } catch (error) {
      console.log(error);

      if (data === []) {
            modalContent.innerHTML = `
        <h3>Список ваших заказов</h3>
        <div class="cart-items">
          <h2>У вас нет заказов</h2>
        </div>`;
        }
    }
  }
});




