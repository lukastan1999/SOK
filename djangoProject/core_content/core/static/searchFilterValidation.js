
function validateSearch() {
    let inputSearch = document.getElementById("searchPolje").value;
    console.log("Vrednost:", inputSearch);
    if (inputSearch === null || inputSearch.trim() === "") {
        alert("Niste popunili polje za pretragu.");
        return false;
    }
    return true;
}

function validateFilter() {
    let fltAtribut = document.getElementById("filterAtribut").value;
    let fltVrednost = document.getElementById("filterVrednost").value;
    if (fltAtribut === null || fltAtribut.trim() === "" || fltVrednost === null || fltVrednost.trim() === "") {
        alert("Niste popunili sva polja za filtriranje.");
        return false;
    }
    return true;
}