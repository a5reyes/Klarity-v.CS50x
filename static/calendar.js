// use js to edit calendar, add days and add button to day for setting up daily planning
// took me 3 hrs just to make the days accurate in the calendar
document.addEventListener('DOMContentLoaded', function() {
    let tbody = document.querySelector('#calendar');
    let week_row = document.querySelector('#week');
    let firstwk = week_row.cloneNode(true);
    let week = week_row.cloneNode(true);
    let count = 0;
    for(let day in days){
        if(count == 7){
            count = 0;
            tbody.appendChild(week);
            week = week_row.cloneNode(true);
        }
        if(week.children[count].id == days[day]){
            week.children[count].innerHTML = `<a href="/plan?day=${day}&month=${month}&year=${year}">${day}</a>`;
            count++;
        } else {
            let firstwk_day_name = days[Object.keys(days)[day - 1]];
            let firstwk_day_num = Object.keys(days)[day - 1];
            firstwk.querySelector(`#${firstwk_day_name}`).innerHTML = `<a href="/plan?day=${firstwk_day_num}&month=${month}&year=${year}">${firstwk_day_num}</a>`;
            let firstwk_days = firstwk.children;
            for (let week_day of firstwk_days){
                if(week_day.innerHTML == `<b>${week_day.id.slice(0, 3)}</b>`){
                    week_day.innerHTML = '';
                }
            }
            tbody.appendChild(firstwk);
        }
    }
    let rem_week = week.children;
    for (let week_day of rem_week){
        if(week_day.innerHTML == `<b>${week_day.id.slice(0, 3)}</b>`){
            week_day.innerHTML = '';
        }
    }
    tbody.appendChild(week);
});
