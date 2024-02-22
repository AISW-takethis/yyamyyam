$(document).ready(function() {
    let selectedDate = new Date(thisDate);

    function refreshDate(date){
    // #this-date에 현재 날짜를 'm월 d일 (요일)'로 출력한다.
        let month = date.getMonth() + 1;
        let day = date.getDate();
        let dayName = ['일', '월', '화', '수', '목', '금', '토'][date.getDay()];
        $('#this-date').text(`${month}월 ${day}일 (${dayName})`);
    }

    function clearCalendar() {
        $('#week-calendar thead').empty(); // 테이블 헤더 초기화
        $('#week-calendar tbody').empty(); // 테이블 바디 초기화
    }

    // date에 해당하는 날짜에 selected_date class를 추가한다.
    function selectDate(date) {
        let month = date.getMonth() + 1;
        let day = date.getDate();
        let year = date.getFullYear();
        let dateString = `${year}${month < 10 ? `0${month}` : month}${day < 10 ? `0${day}` : day}`;
        $(`#${dateString}`).addClass('selected-date');
        $(`#${dateString}a`).addClass('selected-date');
    }

    function generateWeekCalendar(date) {
        clearCalendar();

        const dayNames = ["일", "월", "화", "수", "목", "금", "토"];
        let thead = `<tr>${dayNames.map((day, index) => `<th class='text-center day_calendar_width'${index === 0 ? ' style="color:red"' : ''}>${day}</th>`).join('')}</tr>`;
        $('#week-calendar thead').append(thead);

        const startOfWeek = date.getDate() - date.getDay();
        let weekDay = new Date(date.getFullYear(), date.getMonth(), startOfWeek);

        let tbody = '<tr>';
        for (let i = 0; i < 7; i++) {
            let month = weekDay.getMonth() + 1
            let day = weekDay.getDate();
            let formattedDate = `${weekDay.getFullYear()}${month < 10 ? `0${month}` : month}${day < 10 ? `0${day}` : day}`;// 날짜를 '연월일' 형식으로 포맷팅한다.
            let linkDate = `${weekDay.getFullYear()}-${month < 10 ? `0${month}` : month}-${day < 10 ? `0${day}` : day}`;// 날짜를 '연월일' 형식으로 포맷팅한다.
            let monthDay = weekDay.getDate();
            tbody += `<td id='${formattedDate}' class='text-center day_calendar_width'><a id='${formattedDate}a' href='?date=${linkDate}' ${i === 0 ? ' class="color-error"' : ''}>${monthDay}</a></td>`;
            weekDay.setDate(weekDay.getDate() + 1);
        }
        tbody += '</tr>';
        $('#week-calendar tbody').append(tbody);
    }

    function changeWeek(days) {
        newDate = new Date(selectedDate.setDate(selectedDate.getDate() + days));
        generateWeekCalendar(newDate);
        selectDate(new Date(thisDate));
    }

    $("#prev-week").click(function() {
        changeWeek(-7);
    });

    $("#next-week").click(function() {
        changeWeek(7);
    });

    generateWeekCalendar(selectedDate);
    refreshDate(selectedDate);
    selectDate(selectedDate);
});
