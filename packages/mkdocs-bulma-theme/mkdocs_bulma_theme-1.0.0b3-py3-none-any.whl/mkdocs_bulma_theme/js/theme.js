document.addEventListener("DOMContentLoaded", () => {
  // Get all "navbar-burger" elements
  const $navbarBurgers = Array.prototype.slice.call(
    document.querySelectorAll(".navbar-burger"),
    0
  );

  // Add a click event on each of them
  $navbarBurgers.forEach((el) => {
    el.addEventListener("click", () => {
      // Get the target from the "data-target" attribute
      const target = el.dataset.target;
      const $target = document.getElementById(target);

      // Toggle the "is-active" class on both the "navbar-burger" and the "navbar-menu"
      el.classList.toggle("is-active");
      $target.classList.toggle("is-active");
    });
  });

  // This code is only used to remember theme selection between page loads.
  // The first one is the default.
  const available_themes = ["theme-dark", "theme-light"];

  const themeSwitch = document.querySelector(".theme-switcher");
  let selectedTheme = Number.parseInt(localStorage.getItem("lastTheme"));
  setTheme(selectedTheme);

  /**
   * Toggle the theme of the page.
   */
  function setTheme(index) {
    index = index ?? nextTheme();
    localStorage.setItem("lastTheme", index);
    document.body.classList.remove(...available_themes);
    document.body.classList.add(available_themes[index]);
  }

  /**
   * Gets the next theme index to select.
   *
   * @returns The next theme index to select.
   */
  function nextTheme() {
    if (selectedTheme === null) {
      selectedTheme = 0;
    }

    selectedTheme = (selectedTheme + 1) % available_themes.length;
    return selectedTheme;
  }

  themeSwitch.addEventListener("click", function (e) {
    // const active = e.currentTarget.checked.toString();
    console.debug("Theme switched to %d", selectedTheme + 1);
    setTheme();
  });
});
