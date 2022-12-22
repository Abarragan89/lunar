// Animate the main menu on click
document.getElementById('hamburger').addEventListener('click', () => {
    // Clear out the category submenu if it is showing
    let categoryDivEl = document.getElementById('nav-categories-div')
    if (categoryDivEl.children[0]) {
        categoryDivEl.style.maxHeight = '0'
        while (categoryDivEl.firstChild) {
            categoryDivEl.removeChild(categoryDivEl.firstChild);
        }
    }
    if (document.querySelector('#nav-items-main-div').children[2]) {
        closeMainMenuElements()
        document.getElementById('nav-items-main-div').style.right = '-100vw';
        document.getElementById('nav-items-main-div').style.pointerEvents = 'none';
        
    } else {
        document.getElementById('nav-items-main-div').style.right = '0';
        document.getElementById('nav-items-main-div').style.pointerEvents = 'all';
        createMainMenuElements()
        addListenerToCategories()
    }
})


//  Open and close the navigation submenu on click(the categories)
function addListenerToCategories() {
    document.getElementById('category-nav-btn').addEventListener('click', function () {
        let categoryDivEl = document.getElementById('nav-categories-div')
        if (categoryDivEl.children[0]) {
            categoryDivEl.style.maxHeight = '0'
            while (categoryDivEl.firstChild) {
                categoryDivEl.removeChild(categoryDivEl.firstChild);
            }
        } else {
            document.getElementById('nav-categories-div').style.maxHeight = '500px'
            let allTags = categoryDivEl.getAttribute('data-all-tags')
            allTags = allTags.split(",")
            for (let i = 0; i < allTags.length; i++) {
                let newLI = document.createElement('a')
                newLI.textContent = allTags[i].trim()
                newLI.classList.add('nav-category-item')
                document.getElementById('nav-categories-div').appendChild(newLI)
            }
        }
    })
}

// Create and append the three menu items
function createMainMenuElements () {
   // Create and append the main menu items
   const navCategoryDiv = document.getElementById('nav-categories-div')
   // Profile Link
   const profileBtn = document.createElement('a');
   profileBtn.textContent = "Profile";
   profileBtn.classList.add('main-nav-item');
   profileBtn.href = '/profile';
   navCategoryDiv.insertAdjacentElement('beforebegin', profileBtn);
   // Category Link
   const categoryBtn = document.createElement('a');
   categoryBtn.textContent = 'Categories';
   categoryBtn.href = '#';
   categoryBtn.classList.add('main-nav-item');
   categoryBtn.setAttribute('id', 'category-nav-btn')
   navCategoryDiv.insertAdjacentElement('beforebegin', categoryBtn)
   // Caret Icon
   const caretIcon = document.createElement('i')
   caretIcon.classList.add('fa-sharp', 'fa-solid', 'fa-caret-down');
   // Logout Link
   const logoutBtn = document.createElement('a');
   logoutBtn.textContent = 'Logout';
   logoutBtn.href = "/api/logout"
   logoutBtn.classList.add('main-nav-item');
   navCategoryDiv.insertAdjacentElement('afterEnd', logoutBtn)
}

function closeMainMenuElements() {
    const mainNavItems = document.querySelectorAll('.main-nav-item')
    mainNavItems.forEach(navItem => {
        navItem.remove()
    })
}
