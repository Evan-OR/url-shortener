// Form Refs
const form = document.getElementById("searchForm");
const searchBar = document.getElementById("search");

// Modal Refs
const modal = document.getElementById("modal");
const closeModalBtn = document.getElementById("modal-btn");

modal.addEventListener("click", (e) => {
    const dialogDimensions = modal.getBoundingClientRect();
    if (
        e.clientX < dialogDimensions.left ||
        e.clientX > dialogDimensions.right ||
        e.clientY < dialogDimensions.top ||
        e.clientY > dialogDimensions.bottom
    ) {
        modal.close();
    }
});
closeModalBtn.addEventListener("click", () => modal.close());

const displayModal = (title, message) => {
    const modal = document.getElementById("modal");
    const modalTitle = document.getElementById("modal-title");
    const modalbody = document.getElementById("modal-body");

    modalTitle.innerText = title;
    modalbody.innerText = message;

    modal.showModal();
};

form.addEventListener("submit", async (e) => {
    e.preventDefault();

    // client side validation
    url = searchBar.value;

    if (!hasHTTP(url)) {
        displayModal("Invlid URL", "URL needs to have http:// or https://");
        return;
    }
    if (!isValidURL(url)) {
        displayModal(
            "Invlid URL",
            "Try using a valid URL e.g. https://google.com"
        );
        return;
    }

    const options = {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ url: url }),
    };

    try {
        const req = await fetch(`/create-link`, options);
        if (!req.ok) {
            displayModal(
                "Error Creating Link",
                "We ran into an issue creating your link :("
            );
            return;
        }
        const res = await req.json();

        document.getElementById("res").innerText = JSON.stringify(res);
        window.location.replace(res.shortened);
    } catch (e) {
        displayModal(
            "Error Creating Link",
            "We ran into an issue creating your link :("
        );
    }
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
