// Menu sur téléphone : ouvre et ferme le menu au clic sur le bouton
const buttonMenu = document.querySelector(".site-header_menu");
const menu = document.getElementById("menu-principal");

buttonMenu.addEventListener("click", function () {
    const isOpen = menu.classList.toggle("ouvert");
    buttonMenu.setAttribute("aria-expanded", isOpen);
});