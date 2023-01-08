document.getElementById('choose-year').addEventListener('submit', function(e) {
    e.preventDefault()
    yearToQuery = document.getElementById('year-to-query').value
    window.location.pathname = `/history-year/${yearToQuery}`
})