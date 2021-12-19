import {scrapRace} from "./scrap-race.js";

document.addEventListener("DOMContentLoaded", () => {

    const fisIDInput = document.getElementById("fis_id-single-race");

    const onSubmit = async (event) => {
        event.preventDefault();

        await scrapRace(fisIDInput.value, document.getElementById("details-single-race").checked)
    }

    const form = document.getElementById("form-single-race");
    form.addEventListener("submit", onSubmit)
});