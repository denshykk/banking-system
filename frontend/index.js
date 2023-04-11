function showLoginButton() {
    location.reload();
}

function showLogoutButton() {
    const logoutBtn = document.getElementById('logout-btn');
    const registerBtn = document.getElementById('register-btn');
    const loginBtn = document.getElementById('login-btn');

    logoutBtn.style.display = 'inline-block';
    registerBtn.style.display = 'none';
    loginBtn.style.display = 'none';

    const parent = registerBtn.parentNode;
    parent.insertBefore(logoutBtn, registerBtn);
}

function logoutUser() {
    localStorage.removeItem('authData');
    localStorage.removeItem('authExpiration');
    showLoginButton();
}

function setAuthExpiration(expirationTime) {
    const expiration = new Date();
    expiration.setMinutes(expiration.getMinutes() + expirationTime);
    localStorage.setItem('authExpiration', expiration.toISOString());
}

function createBasicAuthHeader(username, password) {
    const credentials = `${username}:${password}`;
    const encodedCredentials = btoa(credentials);
    return `Basic ${encodedCredentials}`;
}

function checkAuthStatus() {
    const authData = localStorage.getItem('authData');
    const authExpiration = localStorage.getItem('authExpiration');

    if (authData && authExpiration) {
        const expirationDate = new Date(authExpiration);

        if (new Date() < expirationDate) {
            showLogoutButton();
            return;
        }

        localStorage.removeItem('authData');
        localStorage.removeItem('authExpiration');
    }
    showLoginButton();
}

function register(event) {
    event.preventDefault();

    const fullname = document.getElementById('registerName').value.split(' ');

    if (fullname.length < 2) {
        alert('Expected at least first name and last name');
        return;
    }

    const firstName = fullname.at(0);
    const lastName = fullname.at(fullname.length - 1);

    const email = document.getElementById('registerEmail').value;
    const username = document.getElementById('registerUsername').value;
    const password = document.getElementById('registerPassword').value;
    const confirmPassword = document.getElementById('registerConfirmPassword').value;

    if (password.length < 8) {
        alert('Password should be at least 8 characters in length!');
        return;
    }

    if (password !== confirmPassword) {
        alert('Passwords do not match!');
        return;
    }

    const registerUrl = 'http://localhost:8090/users';

    const xhr = new XMLHttpRequest();
    xhr.open('POST', registerUrl);
    xhr.setRequestHeader('Content-Type', 'application/json');

    xhr.onreadystatechange = function () {
        if (xhr.readyState === XMLHttpRequest.DONE) {
            if (xhr.status === 200) {
                alert('Registration successful!');
                const authData = btoa(`${email}:${password}`);
                localStorage.setItem('authData', authData);
                setAuthExpiration(1);
                checkAuthStatus();

                const registerModal = document.getElementById('registerModal');
                registerModal.classList.remove('show');
                registerModal.setAttribute('aria-hidden', 'true');
                const modalBackdrop = document.getElementsByClassName('modal-backdrop')[0];
                modalBackdrop.parentNode.removeChild(modalBackdrop);
                document.body.classList.remove('modal-open');
            } else {
                alert(`Registration failed: ${xhr.statusText}`);
            }
        }
    };

    xhr.onerror = function () {
        alert(`Registration failed: ${xhr.statusText}`);
    };

    xhr.send(JSON.stringify({
        username, firstName, lastName, email, password,
    }));
}

function loginUser(event) {
    event.preventDefault();

    const login = document.getElementById('loginEmail').value;
    const password = document.getElementById('loginPassword').value;

    const loginUrl = 'http://localhost:8090/users/login';

    const xhr = new XMLHttpRequest();
    xhr.open('POST', loginUrl);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.setRequestHeader('Authorization', createBasicAuthHeader(login, password));
    xhr.onload = function () {
        if (xhr.status === 200) {
            const authData = btoa(`${login}:${password}`);
            localStorage.setItem('authData', authData);
            setAuthExpiration(1);
            checkAuthStatus();

            const loginModal = document.getElementById('loginModal');
            loginModal.classList.remove('show');
            loginModal.setAttribute('aria-hidden', 'true');
            const modalBackdrop = document.getElementsByClassName('modal-backdrop')[0];
            modalBackdrop.parentNode.removeChild(modalBackdrop);
            document.body.classList.remove('modal-open');
        } else {
            alert('Login failed! Please verify your login and password');
        }
    };
    xhr.onerror = function () {
        alert(`Login failed: ${xhr.statusText}`);
    };
    xhr.send();
}

document.addEventListener('DOMContentLoaded', () => {
    if (localStorage.getItem('authData')) {
        checkAuthStatus();

    }
}, false);
document.getElementById('registerModal').querySelector('form').addEventListener('submit', register);
document.getElementById('loginModal').querySelector('form').addEventListener('submit', loginUser);
document.getElementById('logout-btn').addEventListener('click', logoutUser);
