

//select elements here and store the result so we don't repeat querySelector operations
question_element = document.querySelector(".question");
card_button = document.querySelector(".card-button");
band_button = document.querySelector(".band-button");
next_button = document.querySelector(".next");
streak_element = document.querySelector(".streak");
high_streak_element = document.querySelector(".high-streak");
initial_feedback_element = document.querySelector(".initial-feedback");
feedback_correctness_element = document.querySelector(".feedback-correctness");
feedback_choice_element = document.querySelector(".feedback-choice");
feedback_name_element = document.querySelector(".feedback-name");

game_state = {
    current_question: "",
    streak: 0,
    feedback_correctness: "NA",
    feedback_name: "NA",
    feedback_choice: "NA",
    high_streak: 0,
}

function resetBody(){
    document.body.classList.remove("correct","incorrect");
}

function showInitialFeedback(){
	initial_feedback_element.classList.remove("hidden");
}

function hideInitialFeedback(){
	initial_feedback_element.classList.add("hidden");

}

function showQuestion(){
    question_element.classList.remove("hidden");
}

function hideQuestion(){
	question_element.classList.add("hidden");
}

function disable_buttons(){
    card_button.disabled = true;
    band_button.disabled = true;
    next_button.disabled = true;
    //next_button.disabled = false;
}

function enable_next_button(){
    next_button.disabled = false;
}

function enable_buttons(){
    card_button.disabled = false;
    band_button.disabled = false;
    next_button.disabled = true;
}


function process_response(obj){
    // hide question to make room for feedback
	hideQuestion();
	// update game state
    game_state.current_question = question_element.innerHTML = obj.name;
    //game_state.streak = streak_element.innerHTML = obj.streak;
    game_state.streak = obj.streak;
    game_state.high_streak = obj.high_streak;
    game_state.feedback_name = feedback_name_element.innerHTML = obj.previous_name;
    game_state.feedback_choice = feedback_choice_element.innerHTML = obj.previous_guess;
    game_state.feedback_correctness = initial_feedback_element.innerHTML = feedback_correctness_element.innerHTML = obj.correctness;

    // apply feedback decoration
	resetBody();
    if(game_state.feedback_correctness != "NA"){
        document.body.classList.add(game_state.feedback_correctness);
    }
    showInitialFeedback();
    enable_next_button();
}

function create_querystring(choice){
    var qstring = "?";
    var name_value = encodeURIComponent(game_state.current_question);
    var choice_value = encodeURIComponent(choice);
    qstring += "name="+name_value;
    qstring += "&choice="+choice_value;
    return qstring;
}

async function guess(url){
    disable_buttons();
    var response = await fetch(url,{credentials:"include"});
    var json = await response.json();
    process_response(json);
}

function updateCurrentStreak(){
    streak_element.innerHTML = game_state.streak;
    high_streak_element.innerHTML = game_state.high_streak;
}

function click_band(){
    var choice_url = quiz_api_url+create_querystring("Band");
    guess(choice_url);
}

function click_card(){
    var choice_url = quiz_api_url+create_querystring("Card");
    guess(choice_url);
}

function click_next(){
    hideInitialFeedback();
    showQuestion();
    enable_buttons();
    // show the new streak only after next is clicked, so user can see old streak and reflect on their loss
    updateCurrentStreak();
    resetBody();
}

card_button.onclick = click_card;
band_button.onclick = click_band;
next_button.onclick = click_next;

// send an initial "guess" request (without a submitted choice) to get the initial question
guess(quiz_api_url).then(function(){
    // don't show feedback for initial load, only for ajax responses triggered by guesses.
    hideInitialFeedback();
    resetBody();
    showQuestion();
    enable_buttons();
    updateCurrentStreak();
})


