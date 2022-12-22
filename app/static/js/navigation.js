// Animate the main menu on click
document.getElementById('hamburger').addEventListener('click', () => {
    if (document.getElementById('nav-items-main-div').style.opacity == '1') {
        document.getElementById('nav-items-main-div').style.opacity = '0';
        document.getElementById('nav-items-main-div').style.pointerEvents = 'none';
        document.querySelectorAll('.main-nav-item').forEach((aTag) => {
            aTag.style.bottom = '200px';
        })
    } else {
        document.getElementById('nav-items-main-div').style.opacity = '1';
        document.getElementById('nav-items-main-div').style.pointerEvents = 'all';
        document.querySelectorAll('.main-nav-item').forEach((aTag) => {
            aTag.style.bottom = 0;
        })
    }
})

//  Navigate the submenu on click
document.getElementById('category-nav-btn').addEventListener('click', () => {
    if(document.querySelector('.nav-category-items').style.fontSize == '1em') {
        document.getElementById('nav-categories').style.transform = 'scale(0)'

        document.querySelectorAll('.nav-category-items').forEach((tag) => {
            tag.style.fontSize = '0';
            tag.style.transform = 'scale(0) translateY(-200px)'
        })
    } else {
        document.getElementById('nav-categories').style.transform = 'scale(1)'
        document.querySelectorAll('.nav-category-items').forEach((tag) => {
            tag.style.fontSize = '1em';
            tag.style.transform = 'scale(1) translateY(0)'
        })
    }

})