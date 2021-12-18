let race_id;


document.addEventListener("DOMContentLoaded", () => {

    const fisIDInput = document.getElementById("fis_id-single-race");

    const onSubmit = (event) => {
        event.preventDefault();
        const url = "scrap_race/";
        const submitButton = document.getElementById("submit");
        submitButton.disabled = true;
        event.target.removeEventListener("submit", onSubmit);

        const body = {
            race_id: fisIDInput.value,
            details: document.getElementById("details-single-race").checked,
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
                console.log(race)
                submitButton.disabled = false;
                event.target.addEventListener("submit", onSubmit)
                const race_name = `${race.fields.place} ${race.fields.hill_size} ${race.fields.date}`
                const container = document.getElementById("content");
                const button = document.createElement("a");
                button.innerHTML = race_name;
                button.href = `download/${race_id}/`;
                button.className = "download__link"
                container.appendChild(button);
            })
            .catch(e => console.log(e))
    }

    const form = document.getElementById("form-single-race");
    form.addEventListener("submit", onSubmit)

    const showForms = (event) => {
        event.preventDefault()
        const formContainers = document.getElementsByClassName("forms__form-container")
        for (let i = 0; i < formContainers.length; i++) {
            formContainers[i].classList.replace("forms__container--show", "forms__container--hide")
        }
        event.target.nextElementSibling.classList.replace("forms__container--hide", "forms__container--show")
    }

    const formHeaders = document.querySelectorAll(".forms__title");
    console.log(formHeaders)
    for (let i = 0; i < formHeaders.length; i++) {
        formHeaders[i].addEventListener("click", showForms);
    }

});



