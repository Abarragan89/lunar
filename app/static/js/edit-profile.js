// edit profile modal logic
document.getElementById('edit-profile-btn').addEventListener('click', () => {
    showModal('edit-user-modal');
})

document.querySelector('#edit-user-modal').addEventListener('click', (e) => {
    const isOutside = e.target.closest('.modal');
    if (!isOutside) {
        closeModal('edit-user-modal');
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
