const searchBox =
    document.getElementById("search-box");

const suggestionsBox =
    document.getElementById("suggestions");


searchBox.addEventListener(
    "keyup",
    async function () {

        const query =
            searchBox.value.trim();

        if(query.length === 0){

            suggestionsBox.innerHTML = "";
            suggestionsBox.style.display = "none";

        return;
    }

        const response =
            await fetch(
                `/autocomplete?q=${query}`
            );

        const suggestions =
            await response.json();

        suggestionsBox.innerHTML = "";

        if (suggestions.length === 0) {

            suggestionsBox.style.display = "none";

        return;

    }

    suggestionsBox.style.display = "block";

    suggestions.forEach(item => {

            const div =
                document.createElement("div");

            div.classList.add(
                "suggestion-item"
            );

            div.innerText = item;

            div.addEventListener(
                "click",
                function(){

                    suggestionsBox.innerHTML = "";
                    suggestionsBox.style.display = "none";

                    searchBox.value = "";

                    window.location.href =
                        `/search?q=${encodeURIComponent(item)}`;

                }
            );

            suggestionsBox.appendChild(div);

        });

    }
);

// -----------------------------------
// SEARCH ON ENTER KEY
// -----------------------------------

searchBox.addEventListener(
    "keydown",
    function(event){

        if(event.key === "Enter"){

            const query =
                searchBox.value.trim();

            if(query){

                searchBox.value = "";

                window.location.href =
                    `/search?q=${encodeURIComponent(query)}`;

            }

        }

    }
);


// -----------------------------------
// CLEAR SEARCH BEFORE LEAVING HOME
// -----------------------------------

window.addEventListener("beforeunload", function () {

    searchBox.value = "";

    suggestionsBox.innerHTML = "";

    suggestionsBox.style.display = "none";

});

// -----------------------------------
// CLEAR SEARCH WHEN LEAVING PAGE
// -----------------------------------

window.addEventListener(

    "pagehide",

    function(){

        searchBox.value = "";

        suggestionsBox.innerHTML = "";

        suggestionsBox.style.display = "none";

    }

);

// -----------------------------------
// HIDE AUTOCOMPLETE WHEN CLICKING OUTSIDE
// -----------------------------------

document.addEventListener(

    "click",

    function(event){

        if(

            !searchBox.contains(event.target)

            &&

            !suggestionsBox.contains(event.target)

        ){

            suggestionsBox.innerHTML = "";

            suggestionsBox.style.display = "none";

        }

    }

);