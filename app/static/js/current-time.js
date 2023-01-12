const timeZone = Intl.DateTimeFormat().resolvedOptions().timeZone

const current_timestamp = new Date().toLocaleString('en-US', { timeZone: timeZone})



document.getElementById('dashboard-current-time').textContent = current_timestamp