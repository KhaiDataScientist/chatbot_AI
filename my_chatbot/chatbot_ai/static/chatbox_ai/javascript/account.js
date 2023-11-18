const register_link = document.getElementById("register-link");
const login_link = document.getElementById("login-link");
const login = document.getElementById('login');
const register = document.getElementById('reg');
const login_active = document.getElementById('login-active');
const register_active = document.getElementById('register-active');

register_link.addEventListener("click", function() {
    login.style.display = "none";
    register.style.display = "block";
    login_active.style.display = "none";
    register_active.style.display = "block";
    document.title = "Đăng ký";

});

login_link.addEventListener("click", function() {
    login.style.display = "block";
    register.style.display = "none";
    login_active.style.display = "block";
    register_active.style.display = "none";
    document.title = "Đăng nhập";
});


