// .expanded 클래스를 가진 모든 요소에 대한 클릭 이벤트 리스너 추가
document.querySelectorAll('.expand').forEach(function(expandedElement) {
    expandedElement.addEventListener('click', function() {
        var nutritionElement = expandedElement.nextElementSibling;

        // this의 자식 요소를 선택한다.
        var icon = this.querySelector('.bi');


        if (this.classList.contains('expanded')) {
            // expanded 클래스 삭제
            this.classList.remove('expanded');
            // icon의 클래스를 변경
            icon.classList.replace('bi-chevron-up', 'bi-chevron-down');

            while(nutritionElement){
                // nutritionElement를 안보이게 변경
                nutritionElement.classList.replace('d-flex','d-none');
                break;
                nutritionElement = nutritionElement.nextElementSibling;
            }
        } else {
            // 클릭된 .expanded 클래스 추가
            this.classList.add('expanded');
            // 아이콘 변경
            icon.classList.replace('bi-chevron-down', 'bi-chevron-up');

            while (nutritionElement) {
                nutritionElement.classList.replace('d-none', 'd-flex');
                break; // .nutrition 클래스를 가진 첫 번째 요소를 숨기고 반복 종료
                nutritionElement = nutritionElement.nextElementSibling;
            }
        }


    });
});

function pageReload() {
        // 현재 페이지 새로고침
        location.reload();
    }