document.getElementById('hamburger').addEventListener('click', () => {
    if (document.getElementById('nav-items').style.opacity == '1') {
        document.getElementById('nav-items').style.opacity = '0';
        document.getElementById('nav-items').style.pointerEvents = 'none';
        document.querySelectorAll('#nav-items a').forEach((aTag) => {
            aTag.style.bottom = '200px';
        })
    } else {
        document.getElementById('nav-items').style.opacity = '1';
        document.getElementById('nav-items').style.pointerEvents = 'all';
        document.querySelectorAll('#nav-items a').forEach((aTag) => {
            aTag.style.bottom = 0;
        })
    }
})

document.getElementById('category-nav-btn').addEventListener('click', () => {
    if(document.getElementById('nav-categories').style.opacity == '1') {
        document.getElementById('nav-categories').style.opacity = '0';
        document.getElementById('nav-categories').style.fontSize = '0';
        document.getElementById('nav-categories').style.width = '0';
        document.querySelector('i').classList.remove('fa-caret-up');
        document.querySelector('i').classList.add('fa-caret-down');
        document.querySelectorAll('#nav-categories a').forEach((tag) => {
            tag.style.display = 'none';
        })
    } else {
        document.getElementById('nav-categories').style.opacity = '1';
        document.getElementById('nav-categories').style.fontSize = '1em';
        document.getElementById('nav-categories').style.width = '100%';
        document.querySelector('i').classList.remove('fa-caret-down');
        document.querySelector('i').classList.add('fa-caret-up');
        document.querySelectorAll('#nav-categories a').forEach((tag) => {
            tag.style.display = 'block';
        })
    }

})