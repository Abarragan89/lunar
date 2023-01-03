document.getElementById('edit-category-btn').addEventListener('click', () => {
    showModal('edit-category');
})


document.querySelector('#edit-category').addEventListener('click', (e) => {
    const isOutside = e.target.closest('.modal');
    if (!isOutside) {
        closeModal('edit-category');
    }
})

// Show confirmation modal / Close confirmation modal
document.getElementById('remove-category-btn').addEventListener('click', function() {
    showModal('confirm-category-remove')
    console.log('hi')
})
document.querySelector('#confirm-category-remove').addEventListener('click', (e) => {
    const isOutside = e.target.closest('.modal');
    if (!isOutside) {
        closeModal('confirm-category-remove');
    }
})