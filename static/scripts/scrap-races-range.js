document.addEventListener("DOMContentLoaded", () => {


    const onSubmit = async (event) => {
        event.preventDefault();

        const start = document.getElementById("from").value;
        const end = document.getElementById("to").value;
        const details =  document.getElementById("details-range-race").checked
        const url = "scrap_races_range/";
        const submitButton = document.getElementById("submit-range");
        submitButton.disabled = true;
        event.target.removeEventListener("submit", onSubmit);

        for (let race_id = start; race_id < end; race_id++) {

            const body = {
                race_id,
                details,
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
    }

    const form = document.getElementById("form-range-races");
    form.addEventListener("submit", onSubmit)
});