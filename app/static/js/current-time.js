
const nth = function(d) {
    if (d > 3 && d < 21) return 'th';
    switch (d % 10) {
      case 1:  return "st";
      case 2:  return "nd";
      case 3:  return "rd";
      default: return "th";
    }
}
const day_date = dayjs()
const current_day_of_week = day_date.format('dddd')
const current_date = day_date.format('D')
const full_month = day_date.format('MMMM')

document.getElementById('dashboard-current-time').textContent = `${current_day_of_week}, ${current_date}${nth(current_date)}`
monthDashEl = document.getElementById('current-month-in-dashboard')
// if there is
if (monthDashEl) {
  monthDashEl.textContent = full_month
}

const today = new Date();
const year = today.getFullYear();
let month = today.getMonth() + 1;
month = month.toString()
document.getElementById('see-all-data-link').href = `/history/${year}-${month.padStart(2, '0')}`