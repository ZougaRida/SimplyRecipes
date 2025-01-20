const filterButtons = document.querySelectorAll("aside button");
filterButtons.forEach((button) => {
    button.addEventListener("click", () => {
        const activeButton = document.querySelector(".active");
        activeButton.classList.remove("active");
        activeButton.classList.add("non-active");

        button.classList.remove("non-active");
        button.classList.add("active");
    });
});