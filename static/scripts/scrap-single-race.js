document.addEventListener("DOMContentLoaded", () => {

    const fisIDInput = document.getElementById("fis_id-single-race");

    const onSubmit = async (event) => {
        event.preventDefault();
        const url = "scrap_race/";
        const submitButton = document.getElementById("submit-single");
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

        await fetch(url, config)
            .then(response => response.json())
            .then(data => {
                const race = JSON.parse(data)[0];
                const race_id = race.pk;
                console.log(race)
                submitButton.disabled = false;
                event.target.addEventListener("submit", onSubmit)
                const race_name = `${race.fields.place} ${race.fields.hill_size} ${race.fields.date}`
                const container = document.getElementById("files-container");
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
});