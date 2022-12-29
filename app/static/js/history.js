document.getElementById('choose-month').addEventListener('change', function() {
    window.location.pathname = `/history/${this.value}`
})