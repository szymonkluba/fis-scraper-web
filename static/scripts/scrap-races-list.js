import {scrapRace} from "./scrap-race.js";

document.addEventListener("DOMContentLoaded", () => {


    const onSubmit = async (event) => {
        const fisIDInputs = document.getElementsByClassName("forms__input-list");
        const fisIDs = Array.from(fisIDInputs).map(input => input.value).filter(value => value > 0);
        event.preventDefault();
        const details = document.getElementById("details-single-race").checked;

        for (const race_id of fisIDs) {
            await scrapRace(race_id, details)
        }
    }

    const form = document.getElementById("form-list-races");
    form.addEventListener("submit", onSubmit)
});