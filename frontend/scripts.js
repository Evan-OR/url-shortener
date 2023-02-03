const errText = document.getElementById('err');

const sendRequest = async (e) => {
  e.preventDefault();
  e.stopPropagation();

  const url = document.getElementById('url');
  const btn = document.getElementById('btn');
  btn.disabled = true;

  if (!url.value) {
    alert('please enter a url');
    console.log('empty');
    btn.disabled = false;
    return;
  }
  if (!isValidHttpUrl(url.value)) {
    errText.style.display = 'block';
    console.log('not valid');
    btn.disabled = false;
    return;
  }

  console.log('valid');
  errText.style.display = 'none';

  //ENDCODE URL
  const encodedURL = encodeURIComponent(url.value);

  const req = await fetch(`http://localhost:8080/create/${encodedURL}`, {
    method: 'post',
  });
  const res = await req.json();

  btn.disabled = false;
  console.log(res);
};

const isValidHttpUrl = (string) => {
  let url;
  try {
    url = new URL(string);
  } catch (_) {
    return false;
  }
  return url.protocol === 'http:' || url.protocol === 'https:';
};

document.getElementById('btn').addEventListener('click', sendRequest, false);
