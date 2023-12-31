// List of accepted zip codes
let zipCodeList = [
    "98132",
    "98135",
    "98136",
    "98137",
    "98138",
    "98139",
    "98140",
    "98142",
    "98143",
    "98144",
    "98146",
    "98147",
];

let zipcodeOutput = {
    "INVALID": "INVALID",
    "CANBEDELIVERED": "CANBEDELIVERED",
    "CANNOTBEDELIVERED": "CANNOTBEDELIVERED"
}

// Activates the delivery checks submit button
function activateDeliveryCheck() {
    document
        .querySelector("#zipCodeCheck form")
        .addEventListener("submit", (event) => {
            event.preventDefault(); // Prevents anything to be in input variable from the start
            // Gets info from the input form 
            let zipInput =
                event.submitter.parentNode.querySelector("#zipNumber").value;
            zipInput = zipInput.split(" ").join(""); //removes spaces from string

            if (zipInput.match(/\D/) != null) {
                // If there are no numbers
                document.querySelector("#output").innerHTML =
                    zipcodeOutput["INVALID"];
            } else if (zipInput.length != 5) {
                // If there are more or less then 5 numbers
                document.querySelector("#output").innerHTML =
                    zipcodeOutput["INVALID"];
            } else if (zipCodeList.includes(zipInput)) {
                // If the zip code is valid
                document.querySelector("#output").innerHTML =
                    zipcodeOutput["CANBEDELIVERED"];
            } else {
                // If the zip code is invalid
                document.querySelector("#output").innerHTML =
                    zipcodeOutput["CANNOTBEDELIVERED"];
            }
        });
};

function changeActiveLangImage(language) {
    let active = document.getElementById("activeLang");
    let replace = document.getElementById(language);

    active.innerText = replace.innerText
};

function changeLanguage(language) {
    if (document.documentElement.lang !== language) { // If the submitted language is not the same as the current language
        generateDocument(language)
    }
}
