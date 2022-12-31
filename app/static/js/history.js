// This is the input date field that shows different months. 
document.getElementById('choose-month').addEventListener('change', function() {
    window.location.pathname = `/history/${this.value}`
})


//////////// logic for openining, closing and filling modal for expired charges ////////////
activity_rows = document.querySelectorAll('.edit-expired-charge-btn'); 
activity_rows.forEach((row) => {
    row.addEventListener('click', () => {
        showModal('edit-expired-charge')
        fillEditMonthlyHistoryFields(row)
    })
})

document.querySelector('#edit-expired-charge').addEventListener('click', (e) => {
    const isOutside = e.target.closest('.modal');
    if (!isOutside) {
        closeModal('edit-expired-charge');
    }
})

function fillEditMonthlyHistoryFields(row) {
    const today = new Date();
    const year = today.getFullYear();
    const day = today.getDate();
    const month = today.getMonth() + 1;
    console.log(row.children[0])
    const currentProductTagId = row.children[0].children[0].children[0].children[0].getAttribute('data-expired-tag-id');
    const currentProductId = row.children[0].children[0].children[0].children[0].getAttribute('data-expired-id');
    const currentProductName = row.children[0].children[0].children[0].children[0].getAttribute('data-description');
    let currentProductPrice = row.children[0].children[0].children[0].children[0].nextElementSibling.textContent;
    currentProductPrice = currentProductPrice.slice(1);
    // I need to convert these dates into year-month to work with date input
    let start_date = row.children[0].children[0].children[2].children[0].textContent;
    let end_date = row.children[0].children[0].children[2].children[1].textContent;
    start_date = start_date.split(" ")[2].split("/")
    start_date = start_date.reverse().join("-")
    end_date = end_date.split(" ")[2].split("/")
    end_date = end_date.reverse().join("-")

    document.getElementById('current-expired-price').value = currentProductPrice;
    document.getElementById('current-expired-tag').value = currentProductTagId;
    document.getElementById('current-expired-name').value = currentProductName;
    document.getElementById('expired-id').value = currentProductId;
    document.getElementById('end-date').setAttribute('max', `${year}-${month}-${day}`);
    document.getElementById('end-date').setAttribute('value', end_date);
    document.getElementById('start-date').setAttribute('max', `${year}-${month}-${day}`);
    document.getElementById('start-date').setAttribute('value', start_date);
}