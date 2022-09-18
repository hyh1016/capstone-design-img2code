const init = () => {
    const uploadButton = document.getElementById('upload-btn');
    const uploadInput = document.getElementById('upload-input')
    uploadButton.addEventListener('click', () => uploadInput.click());
    uploadInput.addEventListener('change', uploadEvent);
}

// TODO
const uploadEvent = (e) => {
    const files = e.currentTarget.files;
    if (!files) return;

    // Image 입력을 받아서
    const file = files[0];

    // Preview 등록
    const reader = new FileReader();
    reader.onload = (e) => {
        createImage(e.target.result, file.name);
    };
    reader.readAsDataURL(file);

    // pix2code API 서버에 요청해서 html 획득

    // 받아온 html을 File로 생성 (File명 == Image명)

    // 다운로드 이벤트

}

const createImage = (src, filename) => {
    const img = document.getElementById('preview-img');
    img.setAttribute('src', src);
    img.setAttribute('data-file', filename);
}

init();
