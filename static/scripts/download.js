export const download = async (event) => {
    event.preventDefault();
    const raceID = event.target.dataset.raceID;

    const body = {
        race_id: raceID
    }

    const config = {
        method: "POST",
        body: JSON.stringify(body)
    }

    await fetch("download/", config)
        .then(response => response.blob())
        .then(file => {
                    const url = URL.createObjectURL(file)
                    const link = document.createElement("a");
                    const inputID = document.getElementById(raceID)
                    link.href = url;
                    link.click();
                    URL.revokeObjectURL(url);
                    event.target.remove();
                    inputID.remove();
        })
        .catch(e => console.error(e))
}