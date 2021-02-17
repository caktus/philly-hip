export default function() {
  const navbarBurger = document.querySelector("#navbar-burger");
  navbarBurger.addEventListener("click", function () {
    const dataTarget = this.dataset.target;
    const target = document.getElementById(dataTarget);
    if (target.classList.contains("is-hidden-touch")) {
      target.classList.remove("is-hidden-touch");
    } else {
      target.classList.add("is-hidden-touch");
    }
  });
};
