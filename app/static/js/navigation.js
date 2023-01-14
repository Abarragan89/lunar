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
        // close menu if there are items showing
        closeMainMenu()

    } else {
        // open menu if there are no items and have underlay for click event exit
        openMainMenu()
    }
})

// Add click event to outside menu so it will close
document.getElementById('nav-menu-underlay').addEventListener('click', (e) => {
    e.stopPropagation()
    closeMainMenu()
})

function closeMainMenu() {
    closeMainMenuElements()
    document.getElementById('')
    document.getElementById('nav-menu-underlay').style.display = 'none'
    document.getElementById('nav-items-main-div').style.right = '-100vw';
    document.getElementById('nav-items-main-div').style.pointerEvents = 'none';
    document.getElementById('main-nav').classList.remove('main-nav-open')
    document.getElementById('main-nav').classList.add('main-nav-closed')
    document.getElementById('nav-items-main-div').style.width = '0'
    document.getElementById('hamburger').classList.remove('fa-solid', 'fa-arrow-right')
    document.getElementById('hamburger').classList.add('fa-solid', 'fa-arrow-left')
    document.getElementById('hamburger').style.paddingRight = '10px';
    document.getElementById('hamburger').style.top = '13px'
    document.getElementById('hamburger').style.borderRadius = '8px 0px 0px 8px';

    // take out in 'Buy me a coffee' link
    const buyMeCoffeeEl = document.getElementById('buy-me-coffee-img')
    buyMeCoffeeEl.style.opacity = '0'

    if (window.location.pathname == '/dashboard') {
        // Need to reinstate pointer events after menu closes to the dashboard charts
        dashboardCanvasEl = document.querySelector('.slideshow-container') 
        dashboardCanvasEl.style.pointerEvents = 'all';
    }


}

function openMainMenu() {
    document.getElementById('nav-menu-underlay').style.display = 'block'
    document.getElementById('nav-items-main-div').style.right = '0';
    document.getElementById('nav-items-main-div').style.pointerEvents = 'all';
    document.getElementById('main-nav').classList.remove('main-nav-closed')
    document.getElementById('main-nav').classList.add('main-nav-open')
    document.getElementById('nav-items-main-div').style.width = '100%'
    document.getElementById('hamburger').classList.remove('fa-solid', 'fa-arrow-left')
    document.getElementById('hamburger').classList.add('fa-solid', 'fa-arrow-right')
    document.getElementById('hamburger').style.paddingRight = `${screen.width - 15}px `;
    document.getElementById('hamburger').style.top = '0px'
    document.getElementById('hamburger').style.borderRadius = '0';
    createMainMenuElements()
    addListenerToCategories()
    if (window.location.pathname == '/dashboard') {
        // Need to reinstate pointer events after menu closes to the dashboard charts
        dashboardCanvasEl = document.querySelector('.slideshow-container') 
        dashboardCanvasEl.style.pointerEvents = 'none';
    }
}


//  Open and close the navigation submenu on click(the categories)
function addListenerToCategories() {
    document.getElementById('category-nav-btn').addEventListener('click', function () {
        let categoryDivEl = document.getElementById('nav-categories-div')
        if (categoryDivEl.children[1]) {
            categoryDivEl.style.maxHeight = '0'
            while (categoryDivEl.firstChild) {
                categoryDivEl.removeChild(categoryDivEl.firstChild);
            }
        } else {
            categoryDivEl.style.maxHeight = '500px'
            let allTags = categoryDivEl.getAttribute('data-all-tags')
            let allTagColor = categoryDivEl.getAttribute('data-all-tags-colors')
            allTags = allTags.split(",")
            allTagColor = allTagColor.split("),")

            for (let i = 0; i < allTags.length; i++) {

                // Create category link in nav
                let newLI = document.createElement('a')
                newLI.textContent = `${allTags[i].trim()} `
                newLI.href = `/categories/${allTags[i].trim()}`
                newLI.classList.add('nav-category-item')

                // Attach color span to category link in nav
                let newTagColor = document.createElement('p');
                newTagColor.style.height = '8px'
                newTagColor.style.fontSize = '.001em';
                newTagColor.style.display = 'inline-block'
                newTagColor.style.width = '20px'
                newTagColor.style.color = 'transparent';
                newTagColor.style.backgroundColor = allTagColor[i];

                // Attach color to tags and tag to category div element
                newLI.appendChild(newTagColor);
                categoryDivEl.appendChild(newLI);
            }
        }
    })
}


// Create and append the three menu items
function createMainMenuElements() {
    if (window.location.pathname === '/dashboard') {
        // need to eliminate pointer events so the underlay can recieve events and close the menu
        dashboardCanvasEl = document.querySelector('.slideshow-container') 
        dashboardCanvasEl.style.pointerEvents = 'none';
    }
    
    // Create and append the main menu items
    const navCategoryDiv = document.getElementById('nav-categories-div')
    
    // Dashboard Link
    const dashboardBtn = document.createElement('a');
    dashboardBtn.textContent = "Dashboard";
    dashboardBtn.classList.add('main-nav-item');
    dashboardBtn.href = '/dashboard';
    navCategoryDiv.insertAdjacentElement('beforebegin', dashboardBtn);
    
    // Profile Link
    const profileBtn = document.createElement('a');
    profileBtn.textContent = "Profile";
    profileBtn.classList.add('main-nav-item');
    profileBtn.href = '/profile';
    navCategoryDiv.insertAdjacentElement('beforebegin', profileBtn);
    
    
    // Category Link
    const categoryBtn = document.createElement('a');
    categoryBtn.textContent = 'Categories';
    categoryBtn.classList.add('main-nav-item');
    categoryBtn.setAttribute('id', 'category-nav-btn');
    navCategoryDiv.insertAdjacentElement('beforebegin', categoryBtn);
    
    // Logout Link
    const logoutBtn = document.createElement('a');
    logoutBtn.textContent = 'Logout';
    logoutBtn.href = "/api/logout"
    logoutBtn.classList.add('main-nav-item');
    navCategoryDiv.insertAdjacentElement('afterEnd', logoutBtn)
    
    // History Link
    // Get current date so link goes straight to current month and year
    const today = new Date();
    const year = today.getFullYear();
    let month = today.getMonth() + 1;
    month = month.toString()
    
    // History Link 
    const historyBtn = document.createElement('a');
    historyBtn.textContent = 'History';
    historyBtn.classList.add('main-nav-item');
    historyBtn.href = `/history/${year}-${month.padStart(2, '0')}`
    historyBtn.setAttribute('id', 'history-nav-btn');
    navCategoryDiv.insertAdjacentElement('afterEnd', historyBtn);

    // bring in 'Buy me a coffee' link
    const buyMeCoffeeEl = document.getElementById('buy-me-coffee-img')
    buyMeCoffeeEl.style.opacity = '1'
    buyMeCoffeeEl.style.zIndex = '999'
}

function closeMainMenuElements() {
    const mainNavItems = document.querySelectorAll('.main-nav-item')
    mainNavItems.forEach(navItem => {
        navItem.remove()
    })
}