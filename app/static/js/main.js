document.addEventListener("DOMContentLoaded", () => {

    const root = document.documentElement;

    const themeToggle =
        document.getElementById("themeToggle");

    const themeIcon =
        document.getElementById("themeIcon");


    function applyTheme(theme) {

        root.setAttribute(
            "data-theme",
            theme
        );


        if (!themeIcon) {
            return;
        }


        if (theme === "dark") {

            themeIcon.className =
                "bi bi-sun-fill";

        } else {

            themeIcon.className =
                "bi bi-moon-fill";
        }
    }


    const savedTheme =
        localStorage.getItem("dps-theme");


    if (savedTheme) {

        applyTheme(savedTheme);

    } else {

        const prefersDark =
            window.matchMedia(
                "(prefers-color-scheme: dark)"
            ).matches;

        applyTheme(
            prefersDark ? "dark" : "light"
        );
    }


    if (themeToggle) {

        themeToggle.addEventListener(
            "click",
            () => {

                const currentTheme =
                    root.getAttribute(
                        "data-theme"
                    );

                const newTheme =
                    currentTheme === "dark"
                        ? "light"
                        : "dark";


                applyTheme(newTheme);

                localStorage.setItem(
                    "dps-theme",
                    newTheme
                );
            }
        );
    }

});