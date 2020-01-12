// sets that hold the suggestions that the user has voted on.
var upvotes = new Set([]);
var downvotes = new Set([]);
var original_upvotes = new Set([]);
var original_downvotes = new Set([]);

// Up- and DownVote button sources.
var upvote_img = "/static/img/upvote.png";

var downvote_img = "/static/img/downvote.png";

var upvote_pressed_img = "/static/img/upvote_pressed.png";

var downvote_pressed_img = "/static/img/downvote_pressed.png";

// saveVotes is executed when the page is refreshed or closed.
window.onbeforeunload = saveVotes;

function fetchOriginalVotes() {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (xhttp.readyState === XMLHttpRequest.DONE) {
            if (xhttp.status === 200) {
                var votes = JSON.parse(xhttp.response);
                var votes_length = votes.length;
                for (var i = 0; i < votes_length; i++) {
                    if (votes[i].vote.value == 1) {
                        upvotes.add(votes[i].vote.suggestion_id);
                        original_upvotes.add(votes[i].vote.suggestion_id);
                        changeButtonImage(document.getElementById("sugUpButton" + votes[i].vote.suggestion_id), upvote_pressed_img);
                    } else {
                        downvotes.add(votes[i].vote.suggestion_id);
                        original_downvotes.add(votes[i].vote.suggestion_id);
                        changeButtonImage(document.getElementById("sugDownButton" + votes[i].vote.suggestion_id), downvote_pressed_img);
                    }
                }
            } else {
                alert('There are no votes given by the user!');
            }
        }
    };
    xhttp.open("GET", "/animals/list_suggested/vote/get_votes", true);
    xhttp.send();
};


function saveVotes() {
    // the updated, or new votes are calculated with a difference of the new votes list from the original/old votes list.
    var updated_or_added_upvotes = difference(upvotes, original_upvotes);
    var updated_or_added_downvotes = difference(downvotes, original_downvotes);

    // the votes to delete are gotten by first taking the difference of the union of the original votes from the union of the updated votes
    var votes_to_delete = difference(union(original_upvotes, original_downvotes), union(upvotes, downvotes));
    // edited votes size should be realistic
    if (votes_to_delete.size + updated_or_added_downvotes.size + updated_or_added_upvotes.size < 500 && votes_to_delete.size + updated_or_added_downvotes.size + updated_or_added_upvotes.size > 0) {
        updated_or_added_downvotes = Array.from(updated_or_added_downvotes);
        updated_or_added_upvotes = Array.from(updated_or_added_upvotes);
        votes_to_delete = Array.from(votes_to_delete);
        var data = JSON.stringify({ "upvotes": updated_or_added_upvotes, "downvotes": updated_or_added_downvotes, "todelete": votes_to_delete })
        postToServer("POST", "/animals/list_suggested/vote/save", data)
    }
    return null;
};

function postToServer(method, source, data) {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (xhttp.readyState === XMLHttpRequest.DONE) {
            if (xhttp.status === 200) {
                var response = JSON.parse(xhttp.response)
                console.log("Viesti saatu" , response)
            } else {
                alert('There are was an error in saving the votes!');
            }
        }
    };
    xhttp.open(method, source, false);
    xhttp.setRequestHeader("Content-type", "application/json; charset=utf-8");
    xhttp.send(data);
};

function difference(setA, setB) {
    var _difference = new Set(setA);
    for (var elem of setB) {
        _difference.delete(elem);
    }
    return _difference;
};

function union(setA, setB) {
    var _union = new Set(setA);
    for (var elem of setB) {
        _union.add(elem);
    }
    return _union;
};

function changeButtonImage(button, image) {
    button.style.backgroundImage = 'url(' + image + ')';
    button.style.backgroundRepeat = "no-repeat";
};


function upVote(suggestion_id) {
    suggestion_id = Number(suggestion_id);
    if (!upvotes.has(suggestion_id)) {
        if (downvotes.has(suggestion_id)) {
            downvotes.delete(suggestion_id);
            changeButtonImage(document.getElementById("sugDownButton" + suggestion_id), downvote_img);
        } else {
            upvotes.add(suggestion_id);
            changeButtonImage(document.getElementById("sugUpButton" + suggestion_id), upvote_pressed_img);
        };
        vote_count = document.getElementById("sug" + suggestion_id + "votes");
        vote_count.firstChild.textContent = String(Number(vote_count.firstChild.textContent) + 1);
    };
};

function downVote(suggestion_id) {
    suggestion_id = Number(suggestion_id);
    if (!downvotes.has(suggestion_id)) {
        if (upvotes.has(suggestion_id)) {
            upvotes.delete(suggestion_id);
            changeButtonImage(document.getElementById("sugUpButton" + suggestion_id), upvote_img);
        } else {
            downvotes.add(suggestion_id);
            changeButtonImage(document.getElementById("sugDownButton" + suggestion_id), downvote_pressed_img);
        };
        vote_count = document.getElementById("sug" + suggestion_id + "votes");
        vote_count.firstChild.textContent = String(Number(vote_count.firstChild.textContent) - 1);
    };
};