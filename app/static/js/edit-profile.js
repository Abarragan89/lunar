// edit profile modal logic
// Edit active salary listners
document.getElementById('edit-active-salary-btn').addEventListener('click', function() {
    if(this.previousElementSibling.textContent === 'none active') {
        showModal('new-salary-modal')
    } else {
        showModal('edit-active-salary-modal');
    }
})

document.querySelector('#edit-active-salary-modal').addEventListener('click', (e) => {
    const isOutside = e.target.closest('.modal');
    if (!isOutside) {
        closeModal('edit-active-salary-modal');
    }
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


// Modal listeners to add new salaries. 
document.getElementById('new-salary-btn').addEventListener('click', function() {
    showModal('new-salary-modal')
})

document.querySelector('#new-salary-modal').addEventListener('click', (e) => {
    const isOutside = e.target.closest('.modal');
    if (!isOutside) {
        closeModal('new-salary-modal');
    }
})

document.getElementById('remove-current-salary-btn').addEventListener('click', (e) => {
    showModal('confirm-salary-remove')
})
document.querySelector('#confirm-salary-remove').addEventListener('click', (e) => {
    const isOutside = e.target.closest('.modal');
    if (!isOutside) {
        closeModal('confirm-salary-remove');
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

// modal to edit categories
category_rows = document.querySelectorAll('.edit-category-btn');
category_rows.forEach((row) => {
    row.addEventListener('click', () => {
        showModal('edit-category-in-profile')
        fillRowsInEditCategoryProfile(row)
    })
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

