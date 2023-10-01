const displayPopUp = (message) => {
    const modal = document.getElementById("modal");

    const popUpText = document.getElementById("pop-up-text");
    popUpText.innerText = message;
    modal.show();

    setTimeout(() => {
        modal.close();
    }, 1000);
};

const copyToClipBoard = () => {
    try {
        const linkDisplay = document.getElementById("link");
        navigator.clipboard.writeText(linkDisplay.innerText);
        displayPopUp("Copied Clipboard");
    } catch (e) {
        displayPopUp("Error Copying To Clipboard");
    }
};

const copybtn = document.getElementById("short-link-wrapper");
copybtn.addEventListener("click", copyToClipBoard);
