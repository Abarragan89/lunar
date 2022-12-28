
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
