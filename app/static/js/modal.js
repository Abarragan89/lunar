// SHOW AND HIDE MODALS
// --- button listeners ---- //
document.getElementById('add-expense-btn').addEventListener('click', () => {
    showModal('expense-modal')
})
document.getElementById('add-category-btn').addEventListener('click', () => {
    showModal('category-modal')
})
document.getElementById('add-cash-btn').addEventListener('click', () => {
    showModal('add-cash-modal')
})

// --- modal listeners to close --- //
document.querySelector('#expense-modal').addEventListener('click', (e) => {
    const isOutside = e.target.closest('.modal')
    if (!isOutside) {
        closeModal('expense-modal')
    }
})
document.querySelector('#category-modal').addEventListener('click', (e) => {
    const isOutside = e.target.closest('.modal')
    if (!isOutside) {
        closeModal('category-modal')
    }
})
document.querySelector('#add-cash-modal').addEventListener('click', (e) => {
    const isOutside = e.target.closest('.modal')
    if (!isOutside) {
        closeModal('add-cash-modal')
    }
})

// --- show / close function -- //
function showModal(id) {
    document.getElementById(id).classList.add('show-modal')
}
function closeModal(id) {
    document.getElementById(id).classList.remove('show-modal')
}