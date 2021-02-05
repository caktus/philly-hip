export default function() {
  const navbarBurger = document.querySelector("#navbar-burger");
  navbarBurger.addEventListener("click", function () {
    const dataTarget = this.dataset.target;
    const target = document.getElementById(dataTarget);
    if (target.classList.contains("is-active")) {
      target.classList.remove("is-active");
    } else {
      target.classList.add("is-active");
    }
  });
};
