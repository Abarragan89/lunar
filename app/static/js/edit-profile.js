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

// modal to edit categories
category_rows = document.querySelectorAll('.edit-category-btn');
category_rows.forEach((row) => {
    row.addEventListener('click', () => {
        showModal('edit-category-in-profile')
        fillRowsInEditCategoryProfile(row)
    })
})

document.querySelector('#edit-category-in-profile').addEventListener('click', (e) => {
    const isOutside = e.target.closest('.modal');
    if (!isOutside) {
        closeModal('edit-category-in-profile');
    }
})

function fillRowsInEditCategoryProfile(row) {
    // Get category data to fill in form
    const categoryId = row.children[0].getAttribute('data-tag-id')
    const categoryColor = row.children[0].getAttribute('data-tag-color')
    const categoryName = row.children[0].textContent
    // populate for with category data
    document.getElementById('category-id-in-profile').value = categoryId
    document.getElementById('category-color-in-profile').value = categoryColor
    document.getElementById('category-name-in-profile').value = categoryName
    // removal options set
    document.getElementById('make-inactive-id').value = categoryId
    document.getElementById('delete-category-id').value = categoryId
}


document.getElementById('remove-category-btn-profile').addEventListener('click', () => {
    showModal('confirm-category-remove-profile');
})

document.querySelector('#confirm-category-remove-profile').addEventListener('click', (e) => {
    const isOutside = e.target.closest('.modal');
    if (!isOutside) {
        closeModal('confirm-category-remove-profile');
    }
})


// event listeners for the inactive categories
inactive_categories = document.querySelectorAll('.edit-inactive-category-btn');
inactive_categories.forEach((row) => {
    row.addEventListener('click', () => {
        categoryId = row.children[0].getAttribute('data-tag-id')
        document.getElementById('make-category-active-id').value = categoryId
        showModal('reactivate-category')
    })
})

document.querySelector('#reactivate-category').addEventListener('click', (e) => {
    const isOutside = e.target.closest('.modal');
    if (!isOutside) {
        closeModal('reactivate-category');
    }
})

document.getElementById('new-salary-btn').addEventListener('click', function() {
    showModal('add-new-salary-modal')
})

document.querySelector('#add-new-salary-modal').addEventListener('click', (e) => {
    const isOutside = e.target.closest('.modal');
    if (!isOutside) {
        closeModal('add-new-salary-modal');
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



function fillRowsInEditCategoryProfile(row) {
    // Get category data to fill in form
    const categoryId = row.children[0].getAttribute('data-tag-id')
    const categoryColor = row.children[0].getAttribute('data-tag-color')
    const categoryName = row.children[0].textContent
    // populate for with category data
    document.getElementById('category-id-in-profile').value = categoryId
    document.getElementById('category-color-in-profile').value = categoryColor
    document.getElementById('category-name-in-profile').value = categoryName
    // removal options set
    document.getElementById('make-inactive-id').value = categoryId
    document.getElementById('delete-category-id').value = categoryId
}


document.getElementById('remove-category-btn-profile').addEventListener('click', () => {
    showModal('confirm-category-remove-profile');
})

document.querySelector('#confirm-category-remove-profile').addEventListener('click', (e) => {
    const isOutside = e.target.closest('.modal');
    if (!isOutside) {
        closeModal('confirm-category-remove-profile');
    }
})


// event listeners for the inactive categories
inactive_categories = document.querySelectorAll('.edit-inactive-category-btn');
inactive_categories.forEach((row) => {
    row.addEventListener('click', () => {
        categoryId = row.children[0].getAttribute('data-tag-id')
        console.log(categoryId)
        document.getElementById('make-category-active-id').value = categoryId
        showModal('reactivate-category')
    })
})

document.querySelector('#reactivate-category').addEventListener('click', (e) => {
    const isOutside = e.target.closest('.modal');
    if (!isOutside) {
        closeModal('reactivate-category');
    }
})

// Event listeners for editing salary
// Select option to auto populate the fields
document.getElementById('salary-displayed').addEventListener('change', function() {
    const salaryOptions = document.querySelectorAll('.salary-options')
    salaryOptions.forEach((option) => {
        // Get the option selected and use it's data attribute to populate fields
        if (option.selected) {
            currentSalaryId = option.dataset.salaryId;
            currentSalaryAmount = option.dataset.salaryAmount;
            currentSalaryStart = option.dataset.salaryStart;
            currentSalaryEnd = option.dataset.salaryEnd;
            currentSalaryIsActive = option.dataset.isActive;

            // need to put a hypen in the date so it works in the date input
            currentSalaryStart = `${currentSalaryStart.slice(0, 4)}-${currentSalaryStart.slice(4)}`
            currentSalaryEnd = `${currentSalaryEnd.slice(0, 4)}-${currentSalaryEnd.slice(4)}`

            document.getElementById('new-monthly-income-edit').value = currentSalaryAmount
            document.getElementById('salary-start-date-edit').value = currentSalaryStart
            document.getElementById('salary-end-date-edit').value = currentSalaryEnd
            document.getElementById('salary-id-delete-data').value = currentSalaryId
            document.getElementById('salary-is-active-delete').value =currentSalaryIsActive

            // If it is the active salary, mark the checkbox
            if (currentSalaryIsActive === "True") {
                document.getElementById('make-active').checked = true;
            } else {
                document.getElementById('make-active').checked = false;
            }

        }
    })
})