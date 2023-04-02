document.addEventListener('DOMContentLoaded', function() {
  const enterBtn = document.querySelector('#enter_btn');

  enterBtn.addEventListener('click', async (event) => {
    //event.preventDefault();
    const email = document.querySelector('#username').value.trim();
    const password = document.querySelector('#password').value.trim();
    const csrftoken = document.cookie.match('(^|;)\\s*csrftoken\\s*=\\s*([^;]+)')?.pop() || '';
    try {
      console.log(email);
      console.log(password);
      console.log(JSON.stringify({email, password}),);
      const response = await fetch('/api/gettoken/', {
        method: 'POST',
        credentials: 'same-origin',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({email, password}),
      });
      const data = await response.json();
      const token = data.token;
      console.log(token);
      if (response.ok) {
        sessionStorage.setItem('token', token);
      } else {
        console.error('Error:', response.detail);
      }

  //
    } catch (error) {
      console.error('Error:', error);
    }
  });


});



        // отправка токена в заголовке Authorization
  //       const productsResponse = await fetch('/api/products/', {
  //         headers: {
  //           'Authorization': `Token ${token}`,
  //         },
  //       });
  //       const products = await productsResponse.json();
  //       console.log(products);
  //     } else {
  //       const error = await response.json();
  //       throw new Error(error.detail);
  //     }
