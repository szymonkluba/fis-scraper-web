export const scrapRace = async (raceID, details) => {
    const body = {
        race_id: raceID,
        details
    }

    const config = {
        method: "POST",
        body: JSON.stringify(body),
    }

    const container = document.getElementById("files-container");
    const filePlaceholder = document.createElement("div");
    const loader = document.createElement("img");
    const label = document.createElement("span");

    label.className = "download__placeholder-label";
    label.innerHTML = `Scrapping race ${raceID}`;

    loader.className = "download__loader";
    loader.src = "static/icons/loader.png";

    filePlaceholder.className = "download__placeholder";
    filePlaceholder.appendChild(label)
    filePlaceholder.appendChild(loader)
    container.appendChild(filePlaceholder)

    await fetch("scrap_race/", config)
        .then(response => response.json())
        .then(data => {
            const race = JSON.parse(data)[0];
            const primaryKey = race.pk;
            const race_name = `${race.fields.place} ${race.fields.hill_size} ${race.fields.date.slice(0, 10)}`
            const button = document.createElement("a");
            const inputID = document.createElement("input");
            inputID.setAttribute("type", "hidden");
            inputID.setAttribute("value", raceID);
            inputID.className = "download__ID";
            button.innerHTML = race_name;
            button.href = `download/${primaryKey}/`;
            button.className = "download__link"
            container.appendChild(button);
            container.appendChild(inputID);
            filePlaceholder.remove();
        })
        .catch(e => {
            console.log(e)
            const failedLabel = document.createElement("span");
            failedLabel.innerHTML = "FAILED";
            failedLabel.className = "download__failed-label";
            loader.remove();
            filePlaceholder.classList.add("download__placeholder--failed");
            filePlaceholder.appendChild(failedLabel);
        })
}