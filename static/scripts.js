let race_id;

const onSubmit = (event) => {
    event.preventDefault()
    const url = "scrap_race/"

    const body = {
        race_id: fisIDInput.value,
        details: true,
    }

    const config = {
        method: "POST",
        body: JSON.stringify(body),
    }

    fetch(url, config)
        .then(response => response.json())
        .then(data => {
            const race = JSON.parse(data)[0];
            race_id = race.pk;
            const container = document.getElementById("content");
            const button = document.createElement("a");
            button.innerHTML = "Download";
            button.href = `download/${race_id}/`;
            container.appendChild(button);
        })
        .catch(e => console.log(e))
}

const form = document.getElementById("form-single-race");
const fisIDInput = document.getElementById("fis_id");


const formContainers = Array.from(document.getElementsByClassName("forms__form-container"))


const showForms = (event) => {
    event.preventDefault()
    for (const container in formContainers) {
        container.classList.replace("forms__container-show", "forms__container--hide")
    }
        event.target.nextElementSibling.classList.replace("forms__container--hide", "forms__container-show")
}

document.addEventListener("DOMContentLoaded", () => {
    const formHeaders = document.querySelectorAll(".forms__title");
    console.log(formHeaders)
    for (let i = 0; 1 < formHeaders.length; i++) {
    formHeaders[i].addEventListener("click", showForms);
}
})

form.addEventListener("submit", onSubmit)

