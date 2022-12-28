document.getElementById('edit-profile-btn').addEventListener('click', () => {
    showModal('edit-user-modal');
})

document.querySelector('#edit-user-modal').addEventListener('click', (e) => {
    const isOutside = e.target.closest('.modal');
    if (!isOutside) {
        closeModal('edit-user-modal');
    }
})

document.querySelector('#new_salary').addEventListener('input', function() {
    if(this.value == '') {
        document.querySelector('#new_salary_date').removeAttribute('required')
    } else {
        document.querySelector('#new_salary_date').setAttribute('required', '')
    }
})

