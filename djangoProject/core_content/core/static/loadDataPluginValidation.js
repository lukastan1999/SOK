file_selected = false;

function validateDataPlugin() {
    let selected = document.getElementById("izvorSelect")
    let val = selected.options[selected.selectedIndex].value;
    if (val === "fajl") {
        if (!file_selected) {
            alert("Niste izabrali fajl.");
            return false;
        }
    } else {
        let inputVal = document.getElementById("urlInput").value;
        if (inputVal === null || inputVal.trim() === "") {
            alert("Niste uneli url adresu.");
            return false;
        }
    }
    return true;

}

function hideUrlShowFile() {
    let url = document.getElementsByClassName("urlCls");
    for (u of url) {
        u.style.display = "none";
    }
    let file = document.getElementById("inputFile");
    file.style.display = '';
}

function showUrlHideFile() {
    let url = document.getElementsByClassName("urlCls");
    for (u of url) {
        u.style.display = '';
    }
    let file = document.getElementById("inputFile");
    file.style.display = "none";

}

function checkIfFajlSelected() {
    let selected = document.getElementById("izvorSelect")
    let val = selected.options[selected.selectedIndex].value;

    if (val === "fajl") {
        hideUrlShowFile();
    } else {
        showUrlHideFile();
    }
}