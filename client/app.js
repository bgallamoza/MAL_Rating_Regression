function get_en_title() {
    var uiTitle = document.getElementById("en_title");
    return uiTitle.value;
}

function get_synopsis() {
    var uiSynopsis = document.getElementById("synopsis");
    return uiSynopsis.value;
}

function get_genres() {
    var genres = [];
    var uiGenres = document.getElementsByName("Genres");
    for (var i in uiGenres) {
        // if a radio button is checked, we increment count
        if (uiGenres[i].checked) {
            genres.push(uiGenres[i].id);
        }
    }
    return JSON.stringify(genres);
}

function get_num_genres() {
    try {
        num = JSON.parse(get_genres()).length
        if (num <= 0) {
            return "";
        } else {
            return num;
        }
    } catch (ex) {
        console.error(ex);
    }
}

function get_extra_studios() {
    var uiExtraStudio = document.getElementById("extra_studio");
    var value = uiExtraStudio.value;
    if (value == "") {
        return 0;
    } else if (parseInt(uiExtraStudio.value) < 0) {
        return "";
    } else {
        return parseInt(uiExtraStudio.value);
    }
}

function get_studios() {
    var studios = [];
    var uiStudios = document.getElementsByName("Studios");
    for (var i in uiStudios) {
        // if a radio button is checked, we increment count
        if (uiStudios[i].checked) {
            studios.push(uiStudios[i].id)
        }
    }
    return JSON.stringify(studios);
}

function get_num_studios() {
    var checkboxes;
    var extra_studios = get_extra_studios();

    try {
        checkboxes = JSON.parse(get_studios()).length;
    } catch (ex) {
        console.error(ex);
    }

    console.log("Checkboxes: ", checkboxes, "  Add_Studios: ", extra_studios);
    if (extra_studios != "" && extra_studios < 0) {
        return "";
    }

    var studios = checkboxes + extra_studios;
    if (studios <= 0) {
        return "";
    } else {
        return studios.toString();
    }
}

function get_source() {
    var uiSource = document.getElementsByName("uiSource");
    for (var i in uiSource) {
        // if a radio button is checked, we return the index + 1
        if (uiSource[i].checked) {
            return uiSource[i].value;
        }
    }
    return ""; // Invalid Value
}

function get_num_related_anime() {
    var uiRelatedAnime = document.getElementById("num_related_anime");
    if (parseInt(uiRelatedAnime.value) < 0) {
        return "";
    } else {
        return uiRelatedAnime.value;
    }
}

function get_num_episodes() {
    var uiEpisodes = document.getElementById("num_episodes");
    if (parseInt(uiEpisodes.value) <= 0) {
        return "";
    } else {
        return uiEpisodes.value;
    }
}

function get_average_episode_duration() {
    var uiDuration = document.getElementById("average_episode_duration");
    if (parseInt(uiDuration.value) <= 0) {
        return "";
    } else {
        return parseInt(uiDuration.value);
    }
}

function get_special_genres(genre) {
    console.log(genre);
    var uiGenre = document.getElementById(genre);
    if (uiGenre.checked) {
        return "1";
    } else {
        return "0";
    }
}

function get_special_studios(studio) {
    console.log(studio);
    var uiStudio = document.getElementById(studio);
    if (uiStudio.checked) {
        return "1";
    } else {
        return "0";
    }
}

function get_other_studio() {
    var uiStudios = document.getElementsByName("Studios");
    var studio_features = [ "EMT Squared", "Bones", "Production I.G", "A-1 Pictures", 
                            "Madhouse", "Kyoto Animation", "Shaft", "DLE"]
    for (var i in uiStudios) {
        // if a radio button is checked, we increment count
        if (uiStudios[i].checked && studio_features.indexOf(uiStudios[i].id) == -1) {
            return "1";
        }
    }
    return "0";
}

function get_columns() {
    console.log("Document loaded");
    var url = "http://127.0.0.1:5000/get_column_info"; // Use if NOT using nginx
    // var url = "/api/get_location_names"; // Use if using nginx
    
    // $ is an alias for jQuery
    // Makes GET call at our url, the response is returned as the data variable
    $.get(url, function(data, status) {
        console.log("Got response for get_column_info request");
        if(data) {
            // "data_columns" is a key in data, which is a JSON
            var data_columns = data.data_columns;
            return data_columns;
        }
    });
}

function post_error(input) {
    var uiError = document.getElementById("uiError");
    switch (input) {
        case "average_episode_duration":
            uiError.innerHTML = "<h3>Your average episode duration must be above 0!</h3>";
            break;
        case "num_episodes":
            uiError.innerHTML = "<h3>You must have at least 1 episode!</h3>";
            break;
        case "title_len":
            uiError.innerHTML = "<h3>Title left blank!</h3>";
            break;
        case "synopsis_len":
            uiError.innerHTML = "<h3>Synopsis left blank!</h3>";
            break;
        case "num_studios":
            uiError.innerHTML = "<h3>Studio input incorrect! Make sure you have at least 1 studio and your extra studio number is positive!</h3>";
            break;
        case "num_genres":
            uiError.innerHTML = "<h3>You need at least 1 genre!</h3>";
            break;
        default:
            uiError.innerHTML = "<h3></h3>";
            break;
    }
}

function on_clicked_rating_pred() {
    console.log("Rating prediction button clicked")
    
    var prediction = document.getElementById("uiRating");
    var url = "http://127.0.0.1:5000/predict_rating"; // Use if NOT using nginx
    // var url = "/api/predict_home_price"; // Use if using nginx

    var form = {};
    var entry_features = ["average_episode_duration", "num_episodes", "synopsis", "en_title",
                        "num_related_anime", "num_genres", "source", "num_studios", "other_studio",
                            "studios", "genres", "extra_studios"]
    var genre_features = ["Drama", "Kids", "Shounen", "Sci-Fi", "Shoujo"];
    var studio_features = [ "EMT Squared", "Bones", "Production I.G", "A-1 Pictures", "Madhouse",
                            "Kyoto Animation", "Shaft", "DLE"];

    for (i in entry_features) {
        // console.log(entry_features[i]);
        form[entry_features[i]] = window["get_" + entry_features[i]];
    }
    for (i in genre_features) {
        form[genre_features[i]] = get_special_genres(genre_features[i]);
    }
    for (i in studio_features) {
        form[studio_features[i]] = get_special_studios(studio_features[i]);
    }

    $.post(url, form, function(data, status) {
        console.log(data.crkcoc_pred);

        // Append this string into the html to show the estimated price
        response = data.rating.toString();
        var isNumber = /\d\.\d\d/.test(response);
        console.log(response, isNumber);
        if (!isNumber) {
            post_error(response);
            prediction.innerHTML = "<h3>Invalid Values!</h3>";
            console.log(status);
        }
        else {
            prediction.innerHTML = "<h3>" + response + "</h3>";
            post_error("");
            console.log(status);
        }
    })
}

function makeList(id, boxNames) {

    $(id).empty(); // Empties the options in drop down
    for (var i in boxNames) {
        var checkbox = document.createElement('input');
        checkbox.type = "checkbox";
        checkbox.name = id.slice(3);
        checkbox.id = boxNames[i];
        var label = document.createElement('label');
        label.htmlFor = boxNames[i];
        label.textContent = boxNames[i];
        
        var list = document.createElement('li');
        list.appendChild(checkbox);
        list.appendChild(label);
        $(id).append(list) // Adds new option
        console.log(boxNames[i]);
    };
}

function onPageLoad() {
    console.log("Document loaded");
    var url = "http://127.0.0.1:5000/get_column_info"; // Use if NOT using nginx
    // var url = "/api/get_location_names"; // Use if using nginx
    
    // $ is an alias for jQuery
    // Makes GET call at our url, the response is returned as the data variable
    $.get(url, function(data, status) {
        console.log("Got response for get_column_info request");
        if(data) {
            var genres = data.genres;
            var studios = data.studios
            makeList('#uiGenres', genres)
            makeList('#uiStudios', studios)
        }
        console.log(status);
    });
}

window.onload = onPageLoad;