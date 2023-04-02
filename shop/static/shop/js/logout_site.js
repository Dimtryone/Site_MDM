document.addEventListener('DOMContentLoaded', function() {
  const logoutBtn = document.getElementById('logout_site')
  logoutBtn.addEventListener("click", function() {
    sessionStorage.removeItem('token');
  });
});


