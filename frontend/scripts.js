const sendRequest = async (e) => {
  if (e) e.preventDefault();

  const url = document.getElementById('url');
  const btn = document.getElementById('btn');
  btn.disabled = true;

  if (!url.value) {
    alert('please enter a url');
    return;
  }

  const req = await fetch(`http://localhost:8080/create/${url.value}`, {
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
