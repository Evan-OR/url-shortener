const sendRequest = async () => {
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
