document.getElementById('download-btn').addEventListener('click', function () {
  const imgElement = document.getElementById('qr');
  const base64Data = imgElement.src; // Get the Base64 data URL
  const mimeType = base64Data.match(/^data:(image\/\w+);base64,/)[1]; // Extract MIME type
  const base64String = base64Data.split(',')[1]; // Extract actual Base64 data

  // Convert Base64 to a Blob
  const byteCharacters = atob(base64String);
  const byteNumbers = new Uint8Array(byteCharacters.length);
  for (let i = 0; i < byteCharacters.length; i++) {
    byteNumbers[i] = byteCharacters.charCodeAt(i);
  }
  const blob = new Blob([byteNumbers], { type: mimeType });
  const blobUrl = URL.createObjectURL(blob);

  // Create a download link and trigger click
  const link = document.createElement('a');
  link.href = blobUrl;
  link.download = 'qr_code.png'; // Set filename
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);

  // Cleanup the object URL
  URL.revokeObjectURL(blobUrl);
  console.log('ran');
});
