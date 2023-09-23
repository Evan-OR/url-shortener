const form = document.getElementById("searchForm");
const searchBar = document.getElementById("search");

form.addEventListener("submit", async (e) => {
    e.preventDefault();

    // client side validation
    url = searchBar.value;

    if (!hasHTTP(url)) {
        alert("URL must start with https:// or http://");
    }
    if (!isValidURL(url)) {
        console.error("Invlid URL");
        return;
    }

    const options = {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ url: url }),
    };

    const req = await fetch(`/create-link`, options);
    const res = await req.json();

    document.getElementById("res").innerText = JSON.stringify(res);
});

const isValidURL = (s) => {
    let url;

    try {
        url = new URL(s);
    } catch (_) {
        return false;
    }

    return true;
};

const hasHTTP = (s) => {
    if (s.indexOf("http://") === -1 && s.indexOf("https://") === -1) {
        return false;
    }

    return true;
};
