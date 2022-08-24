document.addEventListener("DOMContentLoaded", () => {

    const date = new Date();
    let current_year = date.getFullYear();

    console.log(current_year);
    document.querySelector(".year").innerHTML = current_year;

})