
//quiz_api_url = "http://localhost:8000/quiz/quiz";

//select elements here and store the result so we don't repeat querySelector operations
question_element = document.querySelector(".question");
card_button = document.querySelector(".card-button");
band_button = document.querySelector(".band-button");
next_button = document.querySelector(".next");
streak_element = document.querySelector(".streak");
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
}

function resetBody(){
    document.body.classList.remove("correct","incorrect");
}


function showInitialFeedback(){
		initial_feedback_element.style.display = "block";
		//initial_feedback_element.style.width = "auto";
}


function hideInitialFeedback(){
		initial_feedback_element.style.display = "none";
		//initial_feedback_element.style.width = 0;
}


function showQuestion(){
		question_element.style.display = "block";
        //question_element.style.width = "auto";
}


function hideQuestion(){
		question_element.style.display = "none";
		//question_element.style.width = 0;
}


function process_response(obj){
	hideQuestion();
    game_state.current_question = question_element.innerHTML = obj.name;
    game_state.streak = streak_element.innerHTML = obj.streak;
    game_state.feedback_name = feedback_name_element.innerHTML = obj.previous_name;
    game_state.feedback_choice = feedback_choice_element.innerHTML = obj.previous_guess;
    game_state.feedback_correctness = initial_feedback_element.innerHTML = feedback_correctness_element.innerHTML = obj.correctness;
//    console.dir(game_state);
//    console.log(create_querystring("band"));
		resetBody();
    if(game_state.feedback_correctness != "NA"){
        document.body.classList.add(game_state.feedback_correctness);
    }
		showInitialFeedback();
}

function create_querystring(choice){
    var qstring = "?";
    var name_value = encodeURIComponent(game_state.current_question);
    var choice_value = encodeURIComponent(choice);
    qstring += "name="+name_value;
    qstring += "&choice="+choice_value;
    return qstring;
}

function click_band(){
    choice_url = quiz_api_url+create_querystring("Band");
    guess(choice_url);
}

function click_card(){
    choice_url = quiz_api_url+create_querystring("Card");
    guess(choice_url);
}

function click_next(){
		hideInitialFeedback();
		showQuestion();
		enable_buttons();
		resetBody();
}

function guess(url){
    disable_buttons();
    fetch(url,{credentials:"include"}).then(function(data){
        return data.json()
    }).then(function(json){
        //console.dir(json);
        process_response(json);
    })
}

function disable_buttons(){
    card_button.disabled = true;
    band_button.disabled = true;
    next_button.disabled = false;
}

function enable_buttons(){
    card_button.disabled = false;
    band_button.disabled = false;
    next_button.disabled = true;
}

card_button.onclick = click_card;
band_button.onclick = click_band;
next_button.onclick = click_next;


// fetch the initial question and process the response, setting up the quiz for initial use
fetch(quiz_api_url,{credentials:"include"}).then(function(data){
    return data.json()
}).then(function(json){
    //console.dir(json);
    process_response(json);
    // don't show feedback for initial load, only for ajax responses triggered by guesses.
		resetBody();
		hideInitialFeedback();
		showQuestion();
});
