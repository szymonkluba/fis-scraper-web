document.addEventListener("DOMContentLoaded", () => {
    const filesContainer = document.getElementById("files-container");

    const downloadAll = async (event) => {
        event.preventDefault();
        event.stopPropagation();
        if (filesContainer && filesContainer.children.length > 0) {
            const raceIDs = Array.from(filesContainer.querySelectorAll(".download__ID")).map(input => input.value);
            if (raceIDs) {
                const body = {
                race_ids: raceIDs,
            }

            const config = {
                method: "POST",
                body: JSON.stringify(body),
            }
            await fetch("download_all/", config)
                .then(response => response.blob())
                .then(file => {
                    const url = URL.createObjectURL(file)
                    const link = document.createElement("a");
                    link.href = url;
                    link.click();
                    URL.revokeObjectURL(url);
                }).catch(e => console.log(e));
            }
        }
    }

    const downloadAllButton = document.getElementById("download-all");
    downloadAllButton.addEventListener("click", downloadAll);
})