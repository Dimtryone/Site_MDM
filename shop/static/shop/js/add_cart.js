// document.addEventListener('DOMContentLoaded', function() {
//   const addInCartBtn = document.getElementById("add_in_cart");
//   let idProduct = document.getElementById("product_id").textContent;
//   let priceProduct = document.getElementById("price_product").textContent;
//   let nameProduct = document.getElementById("name_product").textContent;
//
//   addInCartBtn.addEventListener("click", function () {
//   let product = {
//     id: idProduct,
//     name: nameProduct,
//     price: priceProduct
//   };
//
//   let cartProducts = localStorage.getItem("cartProducts");
//
//   if (cartProducts && cartProducts.length > 0) {
//     cartProducts = JSON.parse(cartProducts);
//
//     let productIndex = cartProducts.findIndex(p => p.id === product.id);
//
//     if (productIndex !== -1) {
//       let popupHtml = `
//         <div class="popup-dialog">
//           <div class="popup-dialog-content">
//             <h2>Такой товар уже добавлен в корзину</h2>
//             <button class="ok-btn">Закрыть</button>
//           </div>
//         </div>
//       `;
//
//       document.documentElement.insertAdjacentHTML("beforeend", popupHtml);
//
//       let okBtn = document.querySelector(".popup-dialog .ok-btn");
//
//       let popupDialog = document.querySelector('.popup-dialog');
//       window.addEventListener("click", function(event) {
//         if (event.target == popupDialog) {
//           document.querySelector(".popup-dialog").remove();
//         }
//       });
//
//       okBtn.addEventListener("click", function () {
//         document.querySelector(".popup-dialog").remove();
//       });
//
//       return;
//     }
//
//     cartProducts.push(product);
//   } else {
//     cartProducts = [product];
//   }
//
//   localStorage.setItem("cartProducts", JSON.stringify(cartProducts));
//
//   let popupHtml = `
//     <div class="popup-dialog">
//       <div class="popup-dialog-content">
//         <h2>Товар добавлен в корзину</h2>
//         <button class="ok-btn">OK</button>
//       </div>
//     </div>
//   `;
//
//   document.documentElement.insertAdjacentHTML("beforeend", popupHtml);
//
//   let okBtn = document.querySelector(".ok-btn");
//
//   okBtn.addEventListener("click", function () {
//     document.querySelector(".popup-dialog").remove();
//   });
//
//   closeBtn.addEventListener("click", function () {
//     document.querySelector(".popup-dialog").remove();
//   });
// });
// });


