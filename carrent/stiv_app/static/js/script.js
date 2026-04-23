document.addEventListener("DOMContentLoaded", function () {

    const dropBtn = document.querySelector(".dropbtn");
    const dropContent = document.querySelector(".dropdown-content");
    const menuIcon = document.querySelector(".menu-icon");

    dropBtn.onclick = function (event) {
        event.stopPropagation();

        const isOpen = dropContent.classList.toggle("show");

        // Direct toggle without re-checking classList twice
        menuIcon.textContent = isOpen ? "✕" : "☰";
    };

    document.addEventListener("click", function () {
        dropContent.classList.remove("show");
        menuIcon.textContent = "☰";
    });

});