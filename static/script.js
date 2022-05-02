// script.js
// https://stackoverflow.com/questions/35795529/fetch-api-and-multer-error-while-uploading-file
const form = document.getElementById("form");

form.addEventListener("submit", submitForm);

async function console_out(res) {
    out = await res.json()
    console.log(out)
    // location.href = 'newPage.html';
}

document.onload = function(){
    name_el = document.getElementById("name")
    name_el.value = uuidv4()
}()

function uuidv4() {
  return ([1e7]+-1e3+-4e3+-8e3+-1e11).replace(/[018]/g, c =>
    (c ^ crypto.getRandomValues(new Uint8Array(1))[0] & 15 >> c / 4).toString(16)
  );
}

function submitForm(e) {
    e.preventDefault();
    const name = document.getElementById("name");
    const files = document.getElementById("files");
    const formData = new FormData();
    formData.append("name", name.value);
    for(let i =0; i < files.files.length; i++) {
            formData.append("files", files.files[i]);
    }
    fetch("../upload_files", {
        method: 'POST',
        body: formData
    })
        .then((res) => console_out(res))
        .catch((err) => ("Error occured", err));
}