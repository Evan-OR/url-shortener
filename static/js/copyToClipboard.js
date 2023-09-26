const copyToClipBoard = (text) => {
    try {
        navigator.clipboard.writeText(text);
        alert("Copied Clipboard");
    } catch (e) {
        alert("Error Copying To Clipboard");
    }
};

const linkDisplay = document.getElementById("link");
const copyBtn = document.getElementById("copyBtn");
copyBtn.addEventListener("click", () => copyToClipBoard(linkDisplay.innerText));
