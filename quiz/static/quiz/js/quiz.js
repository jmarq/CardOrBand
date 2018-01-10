
quiz_api_url = "http://localhost:8000/quiz/quiz";
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

//current_question = "";

fetch(quiz_api_url,{credentials:"include"}).then(function(data){
    return data.json()
}).then(function(json){
    //console.dir(json);
    process_response(json);
    // don't show feedback for initial load, only for ajax responses triggered by guesses.
    document.body.classList.remove("correct","incorrect");
    initial_feedback_element.style.display = "none";
})

function process_response(obj){
    game_state.current_question = question_element.innerHTML = obj.name;
    game_state.streak = streak_element.innerHTML = obj.streak;
    game_state.feedback_name = feedback_name_element.innerHTML = obj.previous_name;
    game_state.feedback_choice = feedback_choice_element.innerHTML = obj.previous_guess;
    game_state.feedback_correctness = feedback_correctness_element.innerHTML = obj.correctness;
//    console.dir(game_state);
//    console.log(create_querystring("band"));
    initial_feedback_element.innerHTML = game_state.feedback_correctness;
    document.body.classList.remove("correct","incorrect");
    if(game_state.feedback_correctness != "NA"){
        document.body.classList.add(game_state.feedback_correctness);
    }
    initial_feedback_element.style.display = "block";

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

function guess(url){
    disable_buttons();
    fetch(url,{credentials:"include"}).then(function(data){
        return data.json()
    }).then(function(json){
        //console.dir(json);
        process_response(json);
    })
}

card_button.onclick = click_card;
band_button.onclick = click_band;
next_button.onclick = enable_buttons;

function disable_buttons(){
    question_element.style.display = "none";
    card_button.disabled = true;
    band_button.disabled = true;
    next_button.disabled = false;


}

function enable_buttons(){
    question_element.style.display = "block";
    card_button.disabled = false;
    band_button.disabled = false;
    next_button.disabled = true;
    //hide feedback decorations
    initial_feedback_element.style.display="none";
    document.body.classList.remove("correct","incorrect");
}
