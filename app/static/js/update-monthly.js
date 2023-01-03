// Update confirmation modal for monthly charges
document.getElementById('update-monthly-btn').addEventListener('click', () => {
    showModal('confirm-monthly-update');
    fillUpdateConfirmationModal()

})

document.querySelector('#confirm-monthly-update').addEventListener('click', (e) => {
    const isOutside = e.target.closest('.modal');
    if (!isOutside) {
        closeModal('confirm-monthly-update');
    }
})


// This simply gets all the data in the update modal and passes it to the confirmation modal
function fillUpdateConfirmationModal() {
    //  Update moving forward hidden inputs
    document.getElementById('confirm-monthly-update-id').value = document.getElementById('monthly-id').value 
    document.getElementById('confirm-monthly-update-category').value = document.getElementById('current-monthly-tag').value 
    document.getElementById('confirm-monthly-update-price').value = document.getElementById('current-monthly-price').value 
    document.getElementById('confirm-monthly-update-description').value = document.getElementById('current-monthly-name').value 
    document.getElementById('confirm-monthly-update-date').value = document.getElementById('monthly-date-current').value 

    // Completely change history hidden inputs
    document.getElementById('confirm-monthly-update-id-complete').value = document.getElementById('monthly-id').value 
    document.getElementById('confirm-monthly-update-category-complete').value = document.getElementById('current-monthly-tag').value 
    document.getElementById('confirm-monthly-update-price-complete').value = document.getElementById('current-monthly-price').value 
    document.getElementById('confirm-monthly-update-description-complete').value = document.getElementById('current-monthly-name').value 
    document.getElementById('confirm-monthly-update-date-complete').value = document.getElementById('monthly-date-current').value 
}




// Remove confirmation modal for monthly charges
document.getElementById('remove-monthly-btn').addEventListener('click', () => {
    showModal('confirm-monthly-remove');
    fillUpdateRemoveModal()
})

document.querySelector('#confirm-monthly-remove').addEventListener('click', (e) => {
    const isOutside = e.target.closest('.modal');
    if (!isOutside) {
        closeModal('confirm-monthly-remove');
    }
})
// This simply gets all the data in the update modal and passes it to the confirmation modal
function fillUpdateRemoveModal() {
    //  Update moving forward hidden inputs
    document.getElementById('confirm-monthly-delete-id').value = document.getElementById('monthly-id').value 
    document.getElementById('confirm-monthly-delete-category').value = document.getElementById('current-monthly-tag').value 
    document.getElementById('confirm-monthly-delete-price').value = document.getElementById('current-monthly-price').value 
    document.getElementById('confirm-monthly-delete-description').value = document.getElementById('current-monthly-name').value 
    document.getElementById('confirm-monthly-delete-date').value = document.getElementById('monthly-date-current').value 

    // Completely change history hidden inputs
    document.getElementById('confirm-monthly-remove-id-complete').value = document.getElementById('monthly-id').value 
    document.getElementById('confirm-monthly-remove-category-complete').value = document.getElementById('current-monthly-tag').value 
    document.getElementById('confirm-monthly-remove-price-complete').value = document.getElementById('current-monthly-price').value 
    document.getElementById('confirm-monthly-remove-description-complete').value = document.getElementById('current-monthly-name').value 
    document.getElementById('confirm-monthly-remove-date-complete').value = document.getElementById('monthly-date-current').value 
}