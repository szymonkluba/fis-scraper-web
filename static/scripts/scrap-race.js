import { generateDownloadButton } from "./generate-download-button.js";

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
            const { inputID, button } = generateDownloadButton(race);
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