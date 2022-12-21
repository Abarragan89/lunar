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

// Get and format date to restrict date chosen in update
const today = new Date()
const year = today.getFullYear()
const day = today.getDate()
const month = today.getMonth() + 1
function fillEditExpenseFields(row) {
    currentProductTagId = row.children[0].children[1].children[0].getAttribute('data-tag-id')
    currentProductId = row.children[0].children[1].children[0].getAttribute('data-product-id')
    currentProductName = row.children[0].children[1].children[0].nextElementSibling.textContent
    currentProductPrice = row.children[0].children[2].textContent
    current_date = row.children[0].children[0].getAttribute('data-current-date')
    document.getElementById('current-product-price').value = currentProductPrice
    document.getElementById('current-product-tag').value = currentProductTagId
    document.getElementById('current-product-name').value = currentProductName
    document.getElementById('product-id').value = currentProductId
    document.getElementById('expense-date').setAttribute('max', `${year}-${month}-${day}`)
    document.getElementById('expense-date').setAttribute('value', current_date)
}

function fillEditDepositFields(row) {
    currentCashName = row.children[0].children[1].children[0].nextElementSibling.textContent
    currentCashPrice = row.children[0].children[2].textContent
    currentCashId = row.children[0].children[1].children[0].getAttribute('data-cash-id')
    current_date = row.children[0].children[0].getAttribute('data-current-date')
    document.getElementById('current-deposit-amount').value = currentCashPrice
    document.getElementById('current-deposit-description').value = currentCashName
    document.getElementById('cash-id').value = currentCashId
    document.getElementById('deposit-date').setAttribute('max', `${year}-${month}-${day}`)
    document.getElementById('deposit-date').setAttribute('value', current_date)
}
