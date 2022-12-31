// edit profile modal logic
document.getElementById('edit-salary-btn').addEventListener('click', () => {
    showModal('edit-salary-modal');
})

document.querySelector('#edit-salary-modal').addEventListener('click', (e) => {
    const isOutside = e.target.closest('.modal');
    if (!isOutside) {
        closeModal('edit-salary-modal');
    }
})
//  Make salary date required if they enter a new salary. 
document.querySelector('#new_salary').addEventListener('input', function() {
    if(this.value == '') {
        document.querySelector('#new_salary_date').removeAttribute('required')
    } else {
        document.querySelector('#new_salary_date').setAttribute('required', '')
    }
})

// disable and enable update btn depending on whether the user has inputed data. 
document.querySelector('#new_salary').addEventListener('input', function() {
    if (this.value !== '' && document.getElementById('new_salary_date').value !== '') {
        document.getElementById('update-user-btn').disabled = false;
    } else {
        document.getElementById('update-user-btn').disabled = true;
    }
})
document.querySelector('#new_salary_date').addEventListener('input', function() {
    if (this.value !== '' && document.getElementById('new_salary_date').value !== '') {
        document.getElementById('update-user-btn').disabled = false;
    } else {
        document.getElementById('update-user-btn').disabled = true;
    }
})


// modal confirmation button to open confirmation modal
document.querySelector('#update-user-btn').addEventListener('click', () => {
    showModal('confirm-salary-edit')
    fillUpdateUserFields()
})
document.querySelector('#confirm-salary-edit').addEventListener('click', (e) => {
    const isOutside = e.target.closest('.modal');
    if (!isOutside) {
        closeModal('confirm-salary-edit');
    }
})





// Getting data from inital inputs and hiding it in the confirmation modal
function fillUpdateUserFields() {
    document.getElementById('new_salary_update').value = document.getElementById('new_salary').value
    document.getElementById('new_salary_date_update').value = document.getElementById('new_salary_date').value
    document.getElementById('new_salary_update_delete').value = document.getElementById('new_salary').value
    document.getElementById('new_salary_date_update_delete').value = document.getElementById('new_salary_date').value

}


// events to trigger username update
document.getElementById('edit-username-btn').addEventListener('click', function() {
    usernameInputEl = document.getElementById('change-username-input')
    usernameInputEl.disabled = false;
    usernameInputEl.select()
})

// submit form when you are out of blur
document.getElementById('change-username-input').addEventListener('blur', function() {
    document.getElementById('update-username-form').submit()
})
