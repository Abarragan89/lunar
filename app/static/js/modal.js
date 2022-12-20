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

activity_rows = document.querySelectorAll('.edit-activity-btn')
activity_rows.forEach((row) => {
    row.addEventListener('click', () => {
        const typeOfActivity = row.children[0].children[1].children[0].getAttribute('data-type')
        if (typeOfActivity === 'deposit') {
            showModal('edit-deposit')
            fillEditDepositFields(row)
        } else {
            showModal('edit-expense')
            fillEditExpenseFields(row)
        }
    })
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

document.querySelector('#edit-expense').addEventListener('click', (e) => {
    const isOutside = e.target.closest('.modal')
    if (!isOutside) {
        closeModal('edit-expense')
    }
})
document.querySelector('#edit-deposit').addEventListener('click', (e) => {
    const isOutside = e.target.closest('.modal')
    if (!isOutside) {
        closeModal('edit-deposit')
    }
})


// --- show / close function -- //
function showModal(id) {
    document.getElementById(id).classList.add('show-modal')
}
function closeModal(id) {
    document.getElementById(id).classList.remove('show-modal')
}

function fillEditExpenseFields(row) {
    currentProductTagId = row.children[0].children[1].children[0].getAttribute('data-tag-id')
    currentProductName = row.children[0].children[1].children[0].nextElementSibling.textContent
    currentProductPrice = row.children[0].children[2].textContent
    document.getElementById('current-product-price').value = currentProductPrice
    document.getElementById('current-product-tag').value = currentProductTagId
    document.getElementById('current-product-name').value = currentProductName
}

function fillEditDepositFields(row) {
    currentProductName = row.children[0].children[1].children[0].nextElementSibling.textContent
    currentProductPrice = row.children[0].children[2].textContent
    document.getElementById('current-deposit-amount').value = currentProductPrice
    document.getElementById('current-deposit-description').value = currentProductName
}
