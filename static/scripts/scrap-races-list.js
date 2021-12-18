document.addEventListener("DOMContentLoaded", () => {


    const onSubmit = async (event) => {
        const fisIDInputs = document.getElementsByClassName("forms__input-list");
        console.log(fisIDInputs)
        const fisIDs = Array.from(fisIDInputs).map(input => input.value).filter(value => value > 0);
        console.log(fisIDs)
        event.preventDefault();
        const url = "scrap_race/";
        const submitButton = document.getElementById("submit-list");
        submitButton.disabled = true;
        event.target.removeEventListener("submit", onSubmit);
        const details = document.getElementById("details-single-race").checked;

        for (const race_id of fisIDs) {
            const body = {
                race_id,
                details
            }

            const config = {
                method: "POST",
                body: JSON.stringify(body),
            }

            await fetch(url, config)
                .then(response => response.json())
                .then(data => {
                    const race = JSON.parse(data)[0];
                    const raceID = race.pk;
                    console.log(race)
                    submitButton.disabled = false;
                    event.target.addEventListener("submit", onSubmit)
                    const race_name = `${race.fields.place} ${race.fields.hill_size} ${race.fields.date}`
                    const container = document.getElementById("files-container");
                    const button = document.createElement("a");
                    const inputID = document.createElement("input");
                    inputID.setAttribute("type", "hidden");
                    inputID.setAttribute("value", race_id);
                    inputID.className = "download__ID";
                    button.innerHTML = race_name;
                    button.href = `download/${raceID}/`;
                    button.className = "download__link"
                    container.appendChild(button);
                    container.appendChild(inputID);
                })
                .catch(e => console.log(e))
        }
    }

    const form = document.getElementById("form-list-races");
    form.addEventListener("submit", onSubmit)
});