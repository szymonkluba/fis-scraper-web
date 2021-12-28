import {download} from "./download.js";

export const generateDownloadButton = (race) => {
    const primaryKey = race.pk;
    const race_name = `${race.fields.place} ${race.fields.hill_size} ${race.fields.date.slice(0, 10)}`
    const button = document.createElement("a");
    const inputID = document.createElement("input");

    inputID.setAttribute("type", "hidden");
    inputID.setAttribute("value", primaryKey);
    inputID.className = "download__ID";
    inputID.id = primaryKey;

    button.innerHTML = race_name;
    button.href = `#`;
    button.dataset.raceID = primaryKey;
    button.addEventListener("click", download)
    button.className = "download__link";

    return { inputID, button }
}