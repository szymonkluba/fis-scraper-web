import {scrapRace} from "./scrap-race.js";

document.addEventListener("DOMContentLoaded", () => {


    const onSubmit = async (event) => {
        event.preventDefault();
        const start = document.getElementById("from").value;
        const end = document.getElementById("to").value;
        const details =  document.getElementById("details-range-race").checked

        for (let raceID = start; raceID < end; raceID++) {
            await scrapRace(raceID, details)
        }
    }

    const form = document.getElementById("form-range-races");
    form.addEventListener("submit", onSubmit)
});