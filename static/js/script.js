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

window.addEventListener('resize', adjustHeight);
adjustHeight();
