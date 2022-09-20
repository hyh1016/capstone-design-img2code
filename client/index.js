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
    // sending to 34.69.172.233/predict with file post data
    const formData = new FormData();
    formData.append('image', file);

    fetch('http://34.69.172.233/predict', {
        method: 'POST',
        body: formData
    })
    .then(res => res.json())
    .then(res => {
        console.log(res);
        // file.name 확장자 제거
        const filename = file.name.split('.')[0];

        // html 파일 생성
        const blob = new Blob([res.html], {type: 'text/html'});
        const url = URL.createObjectURL(blob);

        // 다운로드 이벤트
        const a = document.createElement('a');
        a.href = url;
        a.download = `${filename}.html`;
        a.click();
    })
    .catch(err => console.log(err));
}

const createImage = (src, filename) => {
    const img = document.getElementById('preview-img');
    img.setAttribute('src', src);
    img.setAttribute('data-file', filename);
}

init();
