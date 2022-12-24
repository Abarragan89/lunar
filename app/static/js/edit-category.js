document.getElementById('edit-category-btn').addEventListener('click', () => {
    showModal('edit-category');
})

document.querySelector('#edit-category').addEventListener('click', (e) => {
    const isOutside = e.target.closest('.modal');
    if (!isOutside) {
        closeModal('edit-category');
    }
})