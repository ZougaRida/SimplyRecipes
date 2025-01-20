const menuIcon = document.querySelector(".menu-icon");
const navGrid = document.querySelector(".navigation-container");
menuIcon.addEventListener("click", () => {
    navGrid.classList.toggle("show-navigation");
    navGrid.classList.toggle("hide-navigation");
});
