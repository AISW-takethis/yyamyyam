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

function convertImgToBase64URL(src, callback, outputFormat) {
    var img = new Image();
    img.crossOrigin = 'Anonymous'; // CORS 이슈를 방지하기 위해 필요할 수 있습니다.
    img.onload = function() {
        var canvas = document.createElement('CANVAS');
        var ctx = canvas.getContext('2d');
        var dataURL;
        canvas.height = this.naturalHeight;
        canvas.width = this.naturalWidth;
        ctx.drawImage(this, 0, 0);
        dataURL = canvas.toDataURL(outputFormat);
        callback(dataURL);
        canvas = null;
    };
    img.src = src;
    if (img.complete || img.complete === undefined) {
        img.src = "data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///ywAAAAAAQABAAACAUwAOw==";
        img.src = src;
    }
}


document.addEventListener('DOMContentLoaded', function () {
    var fileInput = document.querySelector('input[type="file"]');
    var form = document.getElementById('record_form');
    var imagePreview = document.getElementById('imagePreview');
    var upload_text = document.getElementById('upload-text');

    var btnAddDetail = document.getElementById('btn-add-detail');
    var btnEditDetail = document.getElementById('btn-edit-detail');

    if (imagePreview.src === 'http://127.0.0.1:8000/diet/add/' && localStorage.getItem('imagePreview')){
        upload_text.hidden = true;
        imagePreview.hidden = false;

        // base64 to image
        var base64Img = localStorage.getItem('imagePreview');
        imagePreview.src = base64Img;
    }

    if (imagePreview.src !== 'http://127.0.0.1:8000/diet/add/'){
        const imageUrl = imagePreview.src;
        // image to base64
        convertImgToBase64URL(imageUrl, function(base64Img){
            localStorage.setItem('imagePreview', base64Img);
        });
    }

    if (localStorage.getItem('selectedOption')) {
        const selectedOption = localStorage.getItem('selectedOption');
        document.getElementById(selectedOption).checked = true;
    }

    if (localStorage.getItem('mealMemo')) {
        document.getElementById('meal-memo').value = localStorage.getItem('mealMemo');
    }

    if (localStorage.getItem('text-date')) {
        document.getElementById('text-date').value = localStorage.getItem('text-date');
    }

    if (localStorage.getItem('text-time')) {
        document.getElementById('text-time').value = localStorage.getItem('text-time');
    }


    fileInput.addEventListener('change', function (e) {
        var file = e.target.files[0];
        var reader = new FileReader();
        var upload_text = document.getElementById('upload-text');
        reader.onload = function (e) {
            imagePreview.src = e.target.result;
            imagePreview.hidden = false;

            // 이미지 업로드 시에는 이미지 파일의 Base64 데이터를 FormData 객체에 추가하여 전송합니다.
            // 이 때, 이미지 파일의 이름은 'image'로 지정합니다.
            var formData = new FormData();
            formData.append('image', file);

            // 서버에 이미지를 업로드하는 AJAX 요청을 구현합니다.
            // 이 부분은 서버의 엔드포인트 URL과 요청 방식에 따라 달라집니다.
            fetch('/diet/image_process', {
                method: 'POST',
                body: JSON.stringify({image: e.target.result}),
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                }
            }).then(response => response.json())
            .then(data => {
                console.log(data);
            }).catch(error => {
                console.error('Error:', error);
            });
        };
        reader.readAsDataURL(file);
        upload_text.hidden = true;
    });

    form.addEventListener('submit', function (e) {
        e.preventDefault();
        // 여기서 FormData를 사용하여 서버에 이미지를 업로드하는 AJAX 요청을 구현합니다.
        // 이 부분은 서버의 엔드포인트 URL과 요청 방식에 따라 달라집니다.
        alert('서버에 이미지 업로드 구현 필요');
    });

    // localStroage에 저장된 음식 데이터를 가져옵니다.
    var foodInfo = JSON.parse(localStorage.getItem('foodInfo'));

    // 음식 데이터가 있는 경우, HTML에 동적으로 추가합니다.
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
                            <img src="/static/asset/food_images/${food.name}.jpg" class="" alt="${food.name}">
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

    function saveOptionMemo() {
        // 'options'라는 이름을 가진 라디오 버튼들 중에서 선택된 것을 찾습니다.
        const selectedOption = document.querySelector('input[name="options"]:checked');
        const memo = document.getElementById('meal-memo').value;
        const text_date = document.getElementById('text-date').value;
        const text_time = document.getElementById('text-time').value;

        console.log(text_date, text_time);

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

});