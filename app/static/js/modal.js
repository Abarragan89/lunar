// SHOW AND HIDE MODALS
// --- button listeners ---- //
document.getElementById('add-expense-btn').addEventListener('click', () => {
    showModal('expense-modal');
    getCurrentDate('expense-date')
})
document.getElementById('add-category-btn').addEventListener('click', () => {
    showModal('category-modal');
})
document.getElementById('add-cash-btn').addEventListener('click', () => {
    showModal('add-cash-modal');
    getCurrentDate('add-cash-date')
})

function getCurrentDate(id) {
    const today = new Date();
    const year = today.getFullYear();
    let day = today.getDate();
    let month = today.getMonth() + 1;
    month = String(month).padStart(2, '0')
    day = String(day).padStart(2, '0')
    console.log(year, today, day, month)
    document.getElementById(id).setAttribute('max', `${year}-${month}-${day}`);
    document.getElementById(id).setAttribute('value', `${year}-${month}-${day}`);
}

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


// Give each monthly row ability to open modal and call function to fill modal with data
monthly_bill_rows = document.querySelectorAll('.edit-monthly-charge-btn');
monthly_bill_rows.forEach((row) => {
    row.addEventListener('click', () => {
            showModal('edit-monthly-charge');
            fillEditMonthlyFields(row);
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
document.querySelector('#edit-monthly-charge').addEventListener('click', (e) => {
    const isOutside = e.target.closest('.modal');
    if (!isOutside) {
        closeModal('edit-monthly-charge');
    }
})

// --- show / close function -- //
function showModal(id) {
    document.getElementById(id).classList.add('show-modal');
    document.getElementById(id).style.top = `${window.scrollY}px`;
    document.documentElement.style.overflow = 'hidden';
    document.body.scroll = "no";
}
function closeModal(id) {
    document.getElementById(id).classList.remove('show-modal');
    document.documentElement.style.overflow = 'auto';
    document.body.scroll = "yes";
}

function fillEditMonthlyFields(row) {
    const today = new Date();
    const year = today.getFullYear();
    const day = today.getDate();
    const month = today.getMonth() + 1;

    const currentProductTagId = row.children[0].children[1].children[0].getAttribute('data-monthly-tag-id');
    const currentProductId = row.children[0].children[1].children[0].getAttribute('data-monthly-id');
    const currentProductName = row.children[0].children[1].children[0].nextElementSibling.textContent;
    let currentProductPrice = row.children[0].children[2].textContent;
    currentProductPrice = currentProductPrice.slice(1);
    const current_date = row.children[0].children[0].getAttribute('data-current-date');

    document.getElementById('current-monthly-price').value = currentProductPrice;
    document.getElementById('current-monthly-tag').value = currentProductTagId;
    document.getElementById('current-monthly-name').value = currentProductName;
    document.getElementById('monthly-id').value = currentProductId;
    document.getElementById('monthly-date-current').setAttribute('max', `${year}-${month}`);
    document.getElementById('monthly-date-current').setAttribute('value', current_date);
    document.getElementById('stop-monthly-data').value = currentProductId;

}
function fillEditExpenseFields(row) {
    const today = new Date();
    const year = today.getFullYear();
    const day = today.getDate();
    const month = today.getMonth() + 1;

    const currentProductTagId = row.children[0].children[1].children[0].getAttribute('data-tag-id');
    const currentProductId = row.children[0].children[1].children[0].getAttribute('data-product-id');
    const isMonthlyBill = row.children[0].children[1].children[0].getAttribute('data-isMonthly');
    const currentProductName = row.children[0].children[1].children[0].nextElementSibling.textContent;
    let currentProductPrice = row.children[0].children[2].textContent;
    currentProductPrice = currentProductPrice.slice(1);
    const current_date = row.children[0].children[0].getAttribute('data-current-date');

    document.getElementById('current-product-price').value = currentProductPrice;
    document.getElementById('current-product-tag').value = currentProductTagId;
    document.getElementById('current-product-name').value = currentProductName;
    document.getElementById('product-id').value = currentProductId;
    document.getElementById('expense-date-current').setAttribute('max', `${year}-${month}-${day}`);
    document.getElementById('expense-date-current').setAttribute('value', current_date);
    document.getElementById('delete-expense-data').value = currentProductId;
    if (isMonthlyBill === 'True') {
        document.getElementById('monthly-bill-edit').checked = true
    } else {
        document.getElementById('monthly-bill-edit').checked = false
    }
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

