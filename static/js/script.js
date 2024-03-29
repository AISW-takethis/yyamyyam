function adjustHeight() {
    const minWidth = 390; // 최소 너비
    const minHeightRatio = 16 / 9; // 최소 높이 비율
    const viewportHeight = window.innerHeight;
    const viewportWidth = window.innerWidth;

    if (viewportWidth / viewportHeight < minHeightRatio) {
        document.body.style.height = `${viewportWidth / minHeightRatio}px`;
    } else {
        document.body.style.height = '100vh';
    }
}

function updateGoBackButton() {
    // 'nav' 요소의 display 속성 값 가져오기
    var navDisplay = window.getComputedStyle(document.getElementById('main-nav')).display;

    // 'go-back' 버튼 선택
    var goBackButton = document.getElementById('go-back');

    // 'nav'의 display가 'none'이면 'go-back' 버튼에 'd-none' 클래스 추가
    if (navDisplay === 'none') {
        goBackButton.classList.remove('d-none');
    } else {
        // 그렇지 않은 경우, 'd-none' 클래스 제거
        goBackButton.classList.add('d-none');
    }
}


function convertImgToBase64URL(src, outputFormat) {
    return new Promise((resolve, reject) => {
        var img = new Image();
        img.crossOrigin = 'Anonymous';
        img.onload = function() {
            var canvas = document.createElement('CANVAS');
            var ctx = canvas.getContext('2d');
            canvas.height = this.naturalHeight;
            canvas.width = this.naturalWidth;
            ctx.drawImage(this, 0, 0);
            var dataURL = canvas.toDataURL(outputFormat);
            resolve(dataURL);
            canvas = null;
        };
        img.onerror = function() {
            reject(new Error('Could not convert image to Base64'));
        };
        img.src = src;
    });
}


window.addEventListener('resize', adjustHeight);
adjustHeight();

// "go-back" ID를 가진 요소를 찾아서 클릭 이벤트 리스너를 추가
document.getElementById('go-back').addEventListener('click', function() {
    // 뒤로 가기 기능 수행
    window.history.back();
});

updateGoBackButton();


document.getElementById('nav-add').addEventListener('click', function() {
    // localstorage를 비운다.
    localStorage.clear();
});

