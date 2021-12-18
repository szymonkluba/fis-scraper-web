document.addEventListener("DOMContentLoaded", () => {


    const onSubmit = async (event) => {
        const fisIDInputs = document.getElementsByClassName("forms__input-list");
        console.log(fisIDInputs)
        const fisIDs = Array.from(fisIDInputs).map(input => input.value).filter(value => value > 0);
        console.log(fisIDs)
        event.preventDefault();
        const url = "scrap_races_list/";
        const submitButton = document.getElementById("submit-list");
        submitButton.disabled = true;
        event.target.removeEventListener("submit", onSubmit);

        const body = {
            race_ids: fisIDs,
            details: document.getElementById("details-list-race").checked,
        }

        const config = {
            method: "POST",
            body: JSON.stringify(body),
        }

        await fetch(url, config)
            .then(response => response.json())
            .then(data => {
                const races = JSON.parse(data);
                submitButton.disabled = false;
                event.target.addEventListener("submit", onSubmit)

                for (const race of races) {
                    const race_id = race.pk;
                    const race_name = `${race.fields.place} ${race.fields.hill_size} ${race.fields.date}`
                    const container = document.getElementById("files-container");
                    const button = document.createElement("a");
                    button.innerHTML = race_name;
                    button.href = `download/${race_id}/`;
                    button.className = "download__link"
                    container.appendChild(button);
                }
            })
            .catch(e => console.log(e))
    }

    const form = document.getElementById("form-list-races");
    form.addEventListener("submit", onSubmit)
});