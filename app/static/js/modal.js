// SHOW AND HIDE MODALS
// --- button listeners ---- //
document.getElementById('add-expense-btn').addEventListener('click', () => {
    showModal('expense-modal');
})
document.getElementById('add-category-btn').addEventListener('click', () => {
    showModal('category-modal');
})
document.getElementById('add-cash-btn').addEventListener('click', () => {
    showModal('add-cash-modal');
})


// Give each activity row ability to open modal and call function to fill modal with data
activity_rows = document.querySelectorAll('.edit-activity-btn');
activity_rows.forEach((row) => {
    row.addEventListener('click', () => {
        const typeOfActivity = row.children[0].getAttribute('data-type');
        if (typeOfActivity === 'deposit') {
            showModal('edit-deposit');
            fillEditDepositFields(row);
        } else if (typeOfActivity === 'expense') {
            showModal('edit-expense');
            fillEditExpenseFields(row);
            return;
        } else if(typeOfActivity === "edit-in-categories") {
            showModal('edit-expense')
            fillEditExpenseFields(row);
        }
    })
})

// --- modal listeners to close --- //
document.querySelector('#expense-modal').addEventListener('click', (e) => {
    const isOutside = e.target.closest('.modal');
    if (!isOutside) {
        closeModal('expense-modal');
    }
})
document.querySelector('#category-modal').addEventListener('click', (e) => {
    const isOutside = e.target.closest('.modal');
    if (!isOutside) {
        closeModal('category-modal');
    }
})
document.querySelector('#add-cash-modal').addEventListener('click', (e) => {
    const isOutside = e.target.closest('.modal');
    if (!isOutside) {
        closeModal('add-cash-modal');
    }
})

document.querySelector('#edit-expense').addEventListener('click', (e) => {
    const isOutside = e.target.closest('.modal');
    if (!isOutside) {
        closeModal('edit-expense');
    }
})
document.querySelector('#edit-deposit').addEventListener('click', (e) => {
    const isOutside = e.target.closest('.modal');
    if (!isOutside) {
        closeModal('edit-deposit');
    }
})


// --- show / close function -- //
function showModal(id) {
    document.getElementById(id).classList.add('show-modal');
}
function closeModal(id) {
    document.getElementById(id).classList.remove('show-modal');
}

// Get and format date to restrict date chosen in update

function fillEditExpenseFields(row) {
    const today = new Date();
    const year = today.getFullYear();
    const day = today.getDate();
    const month = today.getMonth() + 1;
    const currentProductTagId = row.children[0].children[1].children[0].getAttribute('data-tag-id');
    const currentProductId = row.children[0].children[1].children[0].getAttribute('data-product-id');
    const currentProductName = row.children[0].children[1].children[0].nextElementSibling.textContent;
    let currentProductPrice = row.children[0].children[2].textContent;
    currentProductPrice = currentProductPrice.slice(1);
    const current_date = row.children[0].children[0].getAttribute('data-current-date');
    document.getElementById('current-product-price').value = currentProductPrice;
    document.getElementById('current-product-tag').value = currentProductTagId;
    document.getElementById('current-product-name').value = currentProductName;
    document.getElementById('product-id').value = currentProductId;
    document.getElementById('expense-date').setAttribute('max', `${year}-${month}-${day}`);
    document.getElementById('expense-date').setAttribute('value', current_date);
    document.getElementById('delete-expense-data').value = currentProductId;
}

function fillEditDepositFields(row) {
    const today = new Date();
    const year = today.getFullYear();
    const day = today.getDate();
    const month = today.getMonth() + 1;
    const currentCashName = row.children[0].children[1].children[0].nextElementSibling.textContent;
    let currentCashPrice = row.children[0].children[2].textContent;
    currentCashPrice = currentCashPrice.slice(1);
    const currentCashId = row.children[0].children[1].children[0].getAttribute('data-cash-id');
    const current_date = row.children[0].children[0].getAttribute('data-current-date');
    document.getElementById('current-deposit-amount').value = currentCashPrice;
    document.getElementById('current-deposit-description').value = currentCashName;
    document.getElementById('cash-id').value = currentCashId;
    document.getElementById('deposit-date').setAttribute('max', `${year}-${month}-${day}`);
    document.getElementById('deposit-date').setAttribute('value', current_date);
    document.getElementById('delete-deposit-data').value = currentCashId;
}


// Change transition speed of modals when hovering over button
// This is so modals don't briefly show before they are called
// Get all buttons, then add event listener  that loops through modals and changes their transitions property
allMenuBtns = document.querySelectorAll('menu a');
allMenuBtns.forEach((btn) => {
    btn.addEventListener('mouseenter', () => {
        allModals = document.querySelectorAll('.modal-container');
        allModals.forEach((modal) => {
            modal.style.transition = '.2s';
        })
    })
})

// Get the span elements to give them color on the homepage
allColorSpans = document.querySelectorAll('.tag-color-square')
allColorSpans.forEach(colorSpan => {
    customColor = colorSpan.getAttribute('data-color');
    colorSpan.style.backgroundColor = customColor;
})

