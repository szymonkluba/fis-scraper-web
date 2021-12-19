document.addEventListener("DOMContentLoaded", () => {
    const forms = document.getElementById("forms");
    const filesContainer = document.getElementById("files-container");

    const title = document.getElementById("title");
    const filesTitle = document.getElementById("files-title");

    const scraperLink = document.getElementById("scraper-link");
    const archiveLink = document.getElementById("archive-link");

    const openScraper = (event) => {
        event.preventDefault();
        forms.classList.replace("forms--hide", "forms--show");
        filesContainer.innerHTML = "";
        title.innerHTML = "FIS Scraper";
        filesTitle.innerHTML = "Your files:"
    }

    const openArchive = (event) => {
        event.preventDefault();
        forms.classList.replace("forms--show", "forms--hide");
        filesContainer.innerHTML = "";
        title.innerHTML = "Archive";
        filesTitle.innerHTML = "Archive files:"

        fetch("archive/")
            .then(response => response.json())
            .then(data => {
                    const races = JSON.parse(data).sort((a, b) => a.fields.place > b.fields.place);
                    for (const race of races) {
                        const primaryKey = race.pk;
                        const raceID = race.fields.fis_id;
                        const race_name = `${race.fields.place} ${race.fields.hill_size} ${race.fields.date.slice(0, 10)}`
                        const button = document.createElement("a");
                        const inputID = document.createElement("input");
                        inputID.setAttribute("type", "hidden");
                        inputID.setAttribute("value", raceID);
                        inputID.className = "download__ID";
                        button.innerHTML = race_name;
                        button.href = `download/${primaryKey}/`;
                        button.className = "download__link";
                        filesContainer.appendChild(inputID);
                        filesContainer.appendChild(button);
                    }
                }
            )
    }

    scraperLink.addEventListener("click", openScraper);
    archiveLink.addEventListener("click", openArchive);
})