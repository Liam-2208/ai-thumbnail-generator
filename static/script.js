const videoTitle = document.getElementById('videoTitle');
const styleSelect = document.getElementById('styleSelect');
const imageUpload = document.getElementById('imageUpload');
const generateBtn = document.getElementById('generateBtn');
const thumbnailPreview = document.getElementById('thumbnailPreview');
const downloadLink = document.getElementById('downloadLink');

generateBtn.addEventListener('click', async () => {
  const title = videoTitle.value.trim();
  const style = styleSelect.value;
  const imageFile = imageUpload.files[0];

  if (!title) {
    alert('Please enter a video title.');
    return;
  }

  const formData = new FormData();
  formData.append('title', title);
  formData.append('style', style);
  if (imageFile) {
    formData.append('image', imageFile);
  }

  const response = await fetch('http://127.0.0.1:8000/upload-thumbnail', {
    method: 'POST',
    body: formData
  });

  if (!response.ok) {
    alert('Failed to generate thumbnail.');
    console.error(await response.text());
    return;
  }

  const blob = await response.blob();
  const url = URL.createObjectURL(blob);
  thumbnailPreview.src = url;
  downloadLink.href = url;
});