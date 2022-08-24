document.addEventListener("DOMContentLoaded", () => {

    const date = new Date();
    let current_year = date.getFullYear();

    document.querySelector(".year").innerHTML = current_year;

})