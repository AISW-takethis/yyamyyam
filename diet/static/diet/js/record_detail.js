document.addEventListener('DOMContentLoaded', function() {
    // localStorage에서 음식 정보 가져오기
    const foodInfo = JSON.parse(localStorage.getItem('foodInfo'));

    // 음식 정보가 있는 경우, HTML에 동적으로 추가
    if (foodInfo) {
        const foodContainer = document.getElementById('foodContainer');

        // foodInfo 객체의 각 키(음식 ID)에 대해 반복
        Object.keys(foodInfo).forEach((foodId) => {
            // 현재 음식 ID에 해당하는 음식 정보 가져오기
            const food = foodInfo[foodId];
            caloriePercent = foodInfo[foodId].calorie / 2000 * 100;
            // 음식 상세 정보를 표시하는 HTML 요소 생성
            const foodElement = document.createElement('div');
            foodElement.classList.add('row', 'justify-content-center', 'mb-3', 'py-3', 'border-bottom', 'border-5');

            foodElement.innerHTML = `
                <div class="row py-3 align-items-center">
                    <div class="col-3 text-start">
                        <img src="/static/asset/food_images/${food.name}.jpg" class="detail-food-img"/>
                    </div>
                    <div class="col-9 d-flex flex-column justify-content-between py-2">
                        <div class="row p-0">
                            <h2>${food.name}</h2>
                        </div>
                        <div class="row d-block mb-1 ">
                            <span class="pr-0 fs-1">${food.calorie}</span>
                            <span class="pl-0 grayscale-02">Kcal</span>
                        </div>
                        <div class="row">
                            <div class="col">
                                <div class="progress" style="height: 8px;">
                                    <div class="progress-bar" role="progressbar" aria-label="Example 1px high" style="width: ${caloriePercent}%;" aria-valuenow="{food.calorie}" aria-valuemin="5" aria-valuemax="2000"></div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            `;

            // select 요소
            const selectElement = document.createElement('div');
            selectElement.classList.add('row', 'align-items-center', 'mb-3');

            const selectElement_child = document.createElement('div');
            selectElement_child.classList.add('col-9', 'form-floating');

            const selectElement_child_select = document.createElement('select');
            selectElement_child_select.classList.add('form-select', 'text-center');
            selectElement_child_select.setAttribute('id', 'floatingSelect');
            selectElement_child_select.setAttribute('aria-label', 'Floating label select example');

            // 옵션 값 배열
            const quantities = [0, 0.25, 0.5, 1.0, 1.5, 2.0, 3.0, 4.0, 5.0];

            // 옵션 요소 생성
            quantities.forEach(quantity => {
                const optionElement = document.createElement('option');
                optionElement.value = quantity;
                optionElement.textContent = quantity;

                // food.quantity 값과 일치하는 옵션을 선택 상태로 설정
                if (quantity === food.quantity) {
                    optionElement.selected = true;
                }

                selectElement_child_select.appendChild(optionElement);
            });

            const selectElement_child_label = document.createElement('label');
            selectElement_child_label.classList.add('ms-2');
            selectElement_child_label.setAttribute('for', 'floatingSelect');
            selectElement_child_label.textContent = '인분';

            selectElement_child.appendChild(selectElement_child_select);
            selectElement_child.appendChild(selectElement_child_label);
            selectElement.appendChild(selectElement_child);

            const selectElement_child_btn = document.createElement('div');
            selectElement_child_btn.classList.add('col-3');

            const selectElement_child_btn_grid = document.createElement('div');
            selectElement_child_btn_grid.classList.add('d-grid', 'gap-2');

            const selectElement_child_btn_input = document.createElement('input');
            selectElement_child_btn_input.setAttribute('type', 'submit');
            selectElement_child_btn_input.classList.add('btn', 'btn-outline-primary');
            selectElement_child_btn_input.setAttribute('value', '삭제');

            selectElement_child_btn.appendChild(selectElement_child_btn_grid);
            selectElement_child_btn_grid.appendChild(selectElement_child_btn_input);
            selectElement.appendChild(selectElement_child_btn);

            const changeElement = document.createElement('div');
            changeElement.classList.add('row', 'd-flex', 'justify-content-between', 'align-items-center');
            changeElement.innerHTML = `
                <div class="col">
                    ${food.name}이(가) 아닌가요?
                </div>
                <div class="col text-end">
                    <a href="/diet/detail_search/?item=${foodId}" class="btn btn-secondary" >수정하기</a>
                </div>
            `;

            // foodElement에 select 요소 추가
            foodElement.appendChild(selectElement);
            // foodElement에 change 요소 추가
            foodElement.appendChild(changeElement);
            // 컨테이너에 음식 정보 요소 추가
            foodContainer.appendChild(foodElement);
        });
    }
});
