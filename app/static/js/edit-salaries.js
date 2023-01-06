// --- show / close function -- //
// these two functions would not be seen in modal.js so copy and paste
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


/////////////// Edit old salaries event listeners //////////
// Modal listeners to add new salaries. 

allEditBtns = document.querySelectorAll('.edit-old-salary-btn')
allEditBtns.forEach((row) => {
    row.addEventListener('click', function() {
        showModal('edit-old-salary-modal')
        fillEditSalaryModal(row)
    })
})

document.querySelector('#edit-old-salary-modal').addEventListener('click', (e) => {
    const isOutside = e.target.closest('.modal');
    if (!isOutside) {
        closeModal('edit-old-salary-modal');
    }
})

// populate form fields
function fillEditSalaryModal(row) {
    const salaryId = row.getAttribute('data-set-salary-id')
    const salaryAmount = row.getAttribute('data-set-salary-amount')
    let salaryStart = row.getAttribute('data-set-salary-start')
    let salaryEnd = row.getAttribute('data-set-salary-end')
    // format dates to be strings with dash
    salaryEnd = `${salaryEnd.slice(0,4)}-${salaryEnd.slice(4)}`
    salaryStart = `${salaryStart.slice(0,4)}-${salaryStart.slice(4)}`
    console.log(salaryEnd)

    document.getElementById('edit-salary-income').value = salaryAmount;
    document.getElementById('salary-start-date-edit').value = salaryStart;
    document.getElementById('salary-end-date-edit').value = salaryEnd;
    document.getElementById('salary-id-edit').value = salaryId;
    document.getElementById('salary-id-delete-data').value = salaryId;
}

