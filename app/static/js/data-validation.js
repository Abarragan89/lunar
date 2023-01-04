
document.getElementById('category-form').addEventListener('submit', function(e) {
    const nameInput = document.getElementById('category-name').value
    const pattern = /^[a-z\d\-_\s]+$/i;
    const isNameValid = pattern.test(nameInput)
    if (isNameValid == false) {
        e.preventDefault()
        const errorMessage = document.getElementById('error-msg')
        errorMessage.classList.add('show-error')
        return false
    }
})


if (window.location.pathname === '/') {

} else if (window.location.pathname === '/login') {

} else if (window.location.pathname === '/signin') {
    document.getElementById('signup-form').addEventListener('submit', function(e) {
        const errorEl = document.getElementById('signup-error-msg')
        console.log(errorEl)
        if (errorEl.textContent !== "") {
            e.preventDefault();
            errorEl.classList.add('show-error');
            return false;
        }f
    })
    document.getElementById('signup-email').addEventListener('keydown', function() {
        const errorEl = document.getElementById('signup-error-msg')
        errorEl.textContent = "";
    })
}

// document.getElementById('signup-btn').addEventListener('click', function() {
//     setTimeout(() => {
//         this.disabled = true;
//     }, 50)
// })


// reset password form logic
const passwordRestOne = document.getElementById('password-reset-one')
const passwordRestTwo = document.getElementById('password-reset-two')

passwordRestOne.addEventListener('input', function() {
    if (passwordRestTwo.value == passwordRestOne.value && passwordRestOne.value != '') {
        document.getElementById('confirm-new-password').disabled = false
        console.log('hello')
    } else {
        document.getElementById('confirm-new-password').disabled = true
    }
})

passwordRestTwo.addEventListener('input', function() {
    if (passwordRestOne.value == passwordRestTwo.value && passwordRestTwo.value != '') {
        document.getElementById('confirm-new-password').disabled = false
        console.log('hello')
    } else {
        document.getElementById('confirm-new-password').disabled = true
    }
})
