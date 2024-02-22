function updateList(items) {
        const listGroup = document.getElementById('list-group');
        listGroup.innerHTML = ''; // 리스트 초기화

        Object.keys(items).forEach((key) => {
            const item = items[key];

            const calorie = Math.round(item.calorie);
            const carbohydrate = Math.round(item.carbohydrate * 10) / 10;
            const protein = Math.round(item.protein * 10) / 10;
            const fat = Math.round(item.fat * 10) / 10;

            // 이제 item을 사용하여 작업을 수행할 수 있습니다.
            const li = document.createElement('li');
            li.className = 'list-group-item';
            li.innerHTML = `
                <input class="form-check-input me-1" type="radio" name="listGroupRadio" value="${item.name}" id="${key}" data-calorie=${calorie} data-carbohydrate=${carbohydrate} data-protein=${protein} data-fat=${fat}>
                <label class="form-check-label" for="${key}">${item.name}</label>`;
            listGroup.appendChild(li);
        });
    }

document.addEventListener("DOMContentLoaded", function() {
    const searchAddon = document.getElementById('search-addon');
    const searchBar = document.getElementById('search-bar');
    const searchForm = document.getElementById('search-form');

    const btnConfirm = document.getElementById('btn-confirm');


    searchForm.addEventListener('submit', function(event) {
        event.preventDefault(); // 폼 기본 제출 동작 방지
        const searchTerm = searchBar.value;

        fetch(`/diet/search_items/${encodeURIComponent(searchTerm)}`, {
            method: 'GET',
            headers: {
                'X-Requested-With': 'XMLHttpRequest' // AJAX 요청임을 명시
            }
        }) // URL을 실제 설정한 URL 경로로 변경
        .then(response => response.json())
        .then(data => updateList(data))
        .catch(error => console.error('Error:', error));
    });

    searchAddon.addEventListener('click', function() {
        const searchTerm = searchBar.value;
        fetch(`/diet/search_items/${encodeURIComponent(searchTerm)}`, {
            method: 'GET',
            headers: {
                'X-Requested-With': 'XMLHttpRequest' // AJAX 요청임을 명시
            }
        }) // URL을 실제 설정한 URL 경로로 변경
            .then(response => response.json())
            .then(data => updateList(data))
            .catch(error => console.error('Error:', error));
    });


    btnConfirm.addEventListener('click', async function() {
        const checkedRadio = document.querySelector('input[name="listGroupRadio"]:checked');

        // 현재 페이지 URL의 쿼리 스트링 파싱
        const params = new URLSearchParams(window.location.search);

        if (localStorage.getItem('foodInfo') === null){
            foodInfo = {};
        } else {
            foodInfo = JSON.parse(localStorage.getItem('foodInfo'));
        }


        const foodId = checkedRadio.id;
        const foodName = checkedRadio.value;
        const calorie = checkedRadio.dataset.calorie;
        const carbohydrate = checkedRadio.dataset.carbohydrate;
        const protein = checkedRadio.dataset.protein;
        const fat = checkedRadio.dataset.fat;
        let quantity = 1;
        if (params.has('item')){
            key = params.get('item');
            quantity = foodInfo[key].quantity;
        }

        // 특정 파라미터 값 조회
        const someParam = params.get('item');

        if (params.has('item')){
            // localStorage에서 item을 찾아서 지운다..
            key = params.get('item');
            // localStorage의 foodInfo에서 key에 해당하는 item을 찾아서 지운다.
            foodInfo = JSON.parse(localStorage.getItem('foodInfo'));
            delete foodInfo[key];
        }

        imageUrl = '/static/asset/food_images/' + foodName + '.jpg';

        // 새로운 item을 추가한다.
        try {
            foodImage = await convertImgToBase64URL(imageUrl);
        } catch (error) {
            try {
                imageUrl = '/static/asset/image_plus.png';
                foodImage = await convertImgToBase64URL(imageUrl);
            }
            catch (error) {
                console.error(error);
            }
        }

        foodInfo[foodId] = {
            name: foodName,
            calorie: calorie,
            carbohydrate: carbohydrate,
            protein: protein,
            fat: fat,
            quantity: quantity,
            img: foodImage
        };

        localStorage.setItem('foodInfo', JSON.stringify(foodInfo));


        // record_detail로 이동
        window.location.href = '/diet/detail/';
    });

});
