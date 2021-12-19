document.addEventListener("DOMContentLoaded", () => {

    const showForms = (event) => {
        event.preventDefault()
        const formContainers = document.getElementsByClassName("forms__form-container")
        for (let i = 0; i < formContainers.length; i++) {
            formContainers[i].classList.replace("forms__container--show", "forms__container--hide")
        }
        event.target.nextElementSibling.classList.replace("forms__container--hide", "forms__container--show")
    }

    const formHeaders = document.querySelectorAll(".forms__title");

    for (let i = 0; i < formHeaders.length; i++) {
        formHeaders[i].addEventListener("click", showForms);
    }
})