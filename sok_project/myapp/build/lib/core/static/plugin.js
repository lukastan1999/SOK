let isFileChosen = false;

function pluginDataValidation() {
    const source = document.getElementById("izvorSelect");
    const selectedOption = source.options[source.selectedIndex].value;

    if (selectedOption === "fajl") {
        if (!isFileChosen) {
            alert("Fajl nije izabran.");
            return false;
        }
    } else {
        const urlValue = document.getElementById("urlInput").value;
        if (!urlValue || urlValue.trim() === "") {
            alert("URL nije unet.");
            return false;
        }
    }
    return true;
}

function toggleUrlFileVisibility(displayFile) {
    const urlElements = document.getElementsByClassName("urlCls");
    const fileInput = document.getElementById("inputFile");

    Array.from(urlElements).forEach(urlEl => {
        urlEl.style.display = displayFile ? "none" : "";
    });

    fileInput.style.display = displayFile ? "" : "none";
}

function handleSourceSelection() {
    const sourceElement = document.getElementById("izvorSelect");
    const selectedSource = sourceElement.options[sourceElement.selectedIndex].value;

    if (selectedSource === "fajl") {
        toggleUrlFileVisibility(true);
    } else {
        toggleUrlFileVisibility(false);
    }
}

function fileSelectionChanged() {
    isFileChosen = true;
}
