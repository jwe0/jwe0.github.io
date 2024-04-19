function launch_social(social) {
    if (social === "git") {
        window.open("https://github.com/jwe0"); 
    } else if (social === "mail") {
        window.open("mailto:joshuawebb2007@proton.me");
    } else if (social == "onlymyspace") {
        window.open("https://only-my.space/jwe0");
    }
}

function play() {
    var audio = document.getElementById("myaudio");
    audio.volume = 0.3;
    audio.play();
}


document.addEventListener('click', function() {
    // Remove the blur effect from the body
    document.body.classList.add('blur-off');
    play();
});