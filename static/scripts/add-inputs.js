document.addEventListener("DOMContentLoaded", () => {
    const addButton = document.getElementById("add-inputs");

    let counter = 1;

    const addInputs = (e) => {
        e.preventDefault();
        counter++;
        const inputsWrapper = document.getElementById("inputs-wrapper");

        const label = document.createElement("label");
        label.setAttribute("for", `race_id_${counter}`);
        label.innerHTML = `#${counter} FIS ID:`;

        const form = document.createElement("input");
        form.classList.add("forms__input-list");
        form.setAttribute("type", "number");
        form.setAttribute("name", `race_id_${counter}`);
        form.setAttribute("value", "");
        form.setAttribute("required", "true");
        form.id = `race_id_${counter}`;


        inputsWrapper.appendChild(label);
        inputsWrapper.appendChild(form);
    }

    addButton.addEventListener("click", addInputs)
})