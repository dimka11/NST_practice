// script.js
// https://stackoverflow.com/questions/35795529/fetch-api-and-multer-error-while-uploading-file
const form = document.getElementById("form");

form.addEventListener("submit", submitForm);

let custom_input = document.getElementById("files");
custom_input.addEventListener("change", () => {
    let name = document.getElementById('files');
    if (name.files.length === 2) {
        document.getElementById("filenames").innerHTML = name.files.item(0).name + "<br> " + name.files.item(1).name;
    }
    if (name.files.length === 1) {
        document.getElementById("filenames").innerHTML = name.files.item(0).name + "<br> " + "Нужно загрузить 2 изображения"
    }
})

async function console_out(res) {
    let out = await res.json()
    console.log(out)
    // location.href = 'newPage.html';
}

window.addEventListener('load', () => {
    let name_el = document.getElementById("name")
    name_el.value = uuidv4()
})

function uuidv4() {
  return ([1e7]+-1e3+-4e3+-8e3+-1e11).replace(/[018]/g, c =>
    (c ^ crypto.getRandomValues(new Uint8Array(1))[0] & 15 >> c / 4).toString(16)
  );
}

function submitForm(e) {
    document.getElementById("waiting_message").innerHTML = "Ожидание ..."
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
        .then((res) => {
            // console_out(res)
            const url ='../downloadfile/'+ name.value
             fetch(url)
              .then( res => res.blob() )
              .then( blob => {
                let file = window.URL.createObjectURL(blob);
                // window.location.assign(file);
                let img_container = document.getElementById("final_img");
                img_container.src = file;
                document.getElementById("waiting_message").innerHTML = ""
              });
        })
        .catch((err) => ("Error occurred", err));
}