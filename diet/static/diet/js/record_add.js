function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // 이 쿠키가 요청한 이름과 일치하는지 확인합니다.
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function formatLastModifiedDate(date) {
    const options = {
        year: 'numeric', month: 'long', day: 'numeric',
        hour: 'numeric', minute: 'numeric',
        hour12: true, // 12시간제로 표시
    };
    const formatter = new Intl.DateTimeFormat('ko-KR', options);
    return formatter.format(date);
}

// 날짜를 "YYYY.MM.DD" 형태로 포맷팅하는 함수
function formatDate(date) {
    const options = { year: 'numeric', month: '2-digit', day: '2-digit' };
    const formatter = new Intl.DateTimeFormat('ko-KR', options);
    return formatter.format(date).replaceAll('. ', '.').slice(0, -1); // ". "을 "."으로 변경하고, 마지막 문자 제거
}

// 시간을 "오전/오후 HH:MM" 형태로 포맷팅하는 함수
function formatTime(date) {
    const options = { hour: 'numeric', minute: '2-digit', hour12: true };
    const formatter = new Intl.DateTimeFormat('ko-KR', options);
    return formatter.format(date);
}

function saveOptionMemo() {
    // 'options'라는 이름을 가진 라디오 버튼들 중에서 선택된 것을 찾습니다.
    const selectedOption = document.querySelector('input[name="options"]:checked');
    const memo = document.getElementById('meal-memo').value;
    const text_date = document.getElementById('text-date').value;
    const text_time = document.getElementById('text-time').value;

    if (memo) {
           localStorage.setItem('mealMemo', memo);
    }

    // 선택된 라디오 버튼이 있을 경우, 그 value를 localStorage에 저장합니다.
    if (selectedOption) {
        localStorage.setItem('selectedOption', selectedOption.value);
    }

    if (text_date){
           localStorage.setItem('text-date', text_date);
    }

    if (text_time){
           localStorage.setItem('text-time', text_time);
   }
}

document.addEventListener('DOMContentLoaded', function () {
    var fileInput = document.querySelector('input[type="file"]');
    var form = document.getElementById('record_form');
    var imagePreview = document.getElementById('imagePreview');
    var upload_text = document.getElementById('upload-text');
    var imageBase64 = document.getElementById('image-base64');

    var btnAddDetail = document.getElementById('btn-add-detail');
    var btnEditDetail = document.getElementById('btn-edit-detail');

    // modal 관련 요소
    var modalElement = document.getElementById('staticBackdrop');
    var shootingTimeButton = modalElement.querySelector('#shooting-time-button');
    var currentTimeButton = modalElement.querySelector('#current-time-button');
    var lastModifiedDate = null;
    var takeAt = document.getElementById('text-now');
    var takeDate = document.getElementById('text-date');
    var takeTime = document.getElementById('text-time');

    // loading 관련 요소
    var loading = document.getElementById('loading-modal');

    function changeTakeAt(textDate, textTime, textAt){
        takeDate.value = textDate;
        takeTime.value = textTime;
        takeAt.value = textAt;

        localStorage.setItem('text-date', textDate);
        localStorage.setItem('text-time', textTime);
    }

    // "촬영 시간" 버튼 클릭 이벤트
    shootingTimeButton.addEventListener('click', function () {
        if (lastModifiedDate) {
            console.log(formatDate(lastModifiedDate), formatTime(lastModifiedDate), formatLastModifiedDate(lastModifiedDate));
            changeTakeAt(formatDate(lastModifiedDate), formatTime(lastModifiedDate), formatLastModifiedDate(lastModifiedDate));
            // loding modal의 'd-none' class를 제거하여 화면에 보이게 합니다.
//            loading.classList.remove('d-none');
        } else {
            console.log('파일이 선택되지 않았거나 촬영 시간을 확인할 수 없습니다.');
        }
    });

    // "현재 시간" 버튼 클릭 이벤트
    currentTimeButton.addEventListener('click', function () {
        const currentTime = new Date();
        changeTakeAt(formatDate(currentTime), formatTime(currentTime), formatLastModifiedDate(currentTime));
        // loding modal의 'd-none' class를 제거하여 화면에 보이게 합니다.
        loading.classList.remove('d-none');
    });


    // 이미지 업로드 -> 미리보기
    fileInput.addEventListener('change', function (e) {
        var file = e.target.files[0];
        var reader = new FileReader();
        var upload_text = document.getElementById('upload-text');
        var imageBase64 = document.getElementById('image-base64');
        var modalBody = document.getElementById('modal-body');

        var modal = new bootstrap.Modal(document.getElementById('staticBackdrop'));


        reader.onload = function (e) {
            imagePreview.src = e.target.result;
            imagePreview.hidden = false;
            imageBase64.value = imagePreview.src;
            localStorage.setItem('imagePreview', imagePreview.src);

            lastModifiedDate = new Date(file.lastModified);

            modalBody.innerHTML = `
                ${lastModifiedDate.toLocaleString()}에 촬영된 사진입니다. 촬영 시간 또는 현재 시간을 선택해주세요.
            `;
            modal.show();


            // 이미지 업로드 시에는 이미지 파일의 Base64 데이터를 FormData 객체에 추가하여 전송합니다.
            // 이 때, 이미지 파일의 이름은 'image'로 지정합니다.
            var formData = new FormData();
            formData.append('image', file);


            // 서버에 이미지를 업로드하는 AJAX 요청을 구현합니다.
            // TODO. AI 서버로 보내는 부분!
//            fetch('/diet/image_process', {
//                method: 'POST',
//                body: JSON.stringify({image: e.target.result}),
//                headers: {
//                    'Content-Type': 'application/json',
//                    'X-CSRFToken': getCookie('csrftoken')
//                }
//            }).then(response => response.json())
//            .then(data => {
//                console.log(data);
//            }).catch(error => {
//                console.error('Error:', error);
//            });
        };
        reader.readAsDataURL(file);

        if (upload_text){
            upload_text.hidden = true;
        }
    });

    // localStroage에 저장된 음식 데이터를 가져옵니다.================================================
    // 이미지 관련
    if (localStorage.getItem('imagePreview')){
        if (upload_text){
            upload_text.hidden = true;
        }
        imagePreview.hidden = false;

        // base64 to image
        var base64Img = localStorage.getItem('imagePreview');
        imagePreview.src = base64Img;
        imageBase64.value = imagePreview.src;
    }



    // 메모 관련
    if (localStorage.getItem('mealMemo')) {
        document.getElementById('meal-memo').value = localStorage.getItem('mealMemo');
    }
    // 날짜 및 시간 관련
    if (localStorage.getItem('text-date')) {
        document.getElementById('text-date').value = localStorage.getItem('text-date');
    }
    if (localStorage.getItem('text-time')) {
        document.getElementById('text-time').value = localStorage.getItem('text-time');
    }
    if (localStorage.getItem('takeAt')){
        document.getElementById('text-now').value = localStorage.getItem('takeAt');
    }
    // 음식 종류 관련
    if (localStorage.getItem('selectedOption')) {
        const selectedOption = localStorage.getItem('selectedOption');
        document.getElementById(selectedOption).checked = true;
    }

    // 상세 음식 데이터 관련
    var foodInfo = JSON.parse(localStorage.getItem('foodInfo'));

    if (foodInfo) {
        // 음식 상세 정보 관련 ===================================================
        var foodDetailList = document.getElementById('food-detail-list');
        // foodInfo 객체의 각 키(음식 ID)에 대해 반복합니다.
        Object.keys(foodInfo).forEach(function (foodId) {
            // 현재 음식 ID에 해당하는 음식 정보를 가져옵니다.
            var food = foodInfo[foodId];

            // 음식 상세 정보를 표시하는 HTML 요소를 생성합니다.
            var foodElement = document.createElement('div');
            foodElement.classList.add('col-3');;
            foodElement.innerHTML = `
                        <div class="row">
                            <img src="${food.img}" alt="${food.name}">
                            <input type="hidden" name="fd-${foodId}-img" value="${food.img}">
                            <input type="hidden" name="fd-${foodId}-name" value="${food.name}">
                            <input type="hidden" name="fd-${foodId}-calorie" value="${food.calorie}">
                            <input type="hidden" name="fd-${foodId}-carbohydrate" value="${food.carbohydrate}">
                            <input type="hidden" name="fd-${foodId}-protein" value="${food.protein}">
                            <input type="hidden" name="fd-${foodId}-fat" value="${food.fat}">
                            <input type="hidden" name="fd-${foodId}-quantity" value="${food.quantity}">
                        </div>
                        <div class="row justify-content-center">
                            ${food.name}
                        </div>
                `
            foodDetailList.appendChild(foodElement);
        });

        // 칼로리 관련 ====================================================================
        var totalCalories = 0;
        var totalCarbs = 0;
        var totalProtein = 0;
        var totalFat = 0;

        Object.keys(foodInfo).forEach(function (foodId) {
            var food = foodInfo[foodId];
            totalCalories += parseInt(food.calorie);
            totalCarbs += Math.round(parseFloat(food.carbohydrate)*10)/10;
            totalProtein += Math.round(parseFloat(food.protein)*10)/10;
            totalFat += Math.round(parseFloat(food.fat)*10)/10;
        });

        totalCarbs = Math.round(totalCarbs*10)/10;
        totalProtein = Math.round(totalProtein*10)/10;
        totalFat = Math.round(totalFat*10)/10;

        document.getElementById('total-calories').innerHTML = `${totalCalories}Kcal`;

        const totalNutrition = document.getElementById('total-nutrition');

        totalNutrition.innerHTML = `탄수화물: ${totalCarbs}g, 단백질: ${totalProtein}g, 지방: ${totalFat}g`;
    }

    // 'btn-edit-detail' 버튼에 대한 클릭 이벤트 리스너 추가
    document.getElementById('btn-edit-detail').addEventListener('click', function() {
        saveOptionMemo();
    });

    // 'btn-add-detail' 버튼에 대한 클릭 이벤트 리스너 추가
    document.getElementById('btn-add-detail').addEventListener('click', function() {
        saveOptionMemo();
    });

    var bgGood = document.getElementById('bg-good');
    var bgGoodText = document.getElementById('total-nutrition');

    if (bgGoodText.textContent !== '' && bgGoodText.textContent !== '탄수화물: 0g, 단백질: 0g, 지방: 0g'){
        // bgGood을 보여준다.
        bgGood.hidden = false;
    }

});