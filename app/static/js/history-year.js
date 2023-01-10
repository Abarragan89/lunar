document.getElementById('choose-year-form').addEventListener('submit', function(e) {
    e.preventDefault()
    yearToQuery = document.getElementById('year-to-query').value
    window.location.pathname = `/history-year/${yearToQuery}`
})