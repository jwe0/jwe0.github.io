var pressed = false


function launch_social(social) {
    if (social === "git") {
        window.location.href = "https://github.com/jwe0"; 
    } else if (social === "mail") {
        window.location.href = "mailto:joshuawebb2007@proton.me";
    } else if (social == "onlymyspace") {
        window.location.href = "https://only-my.space/jwe0";
    } else if(social == "blog") {
        window.location.href = "/Blogs";
    } else if(social == "portfolio") {
        window.location.href = "/Portfolio"
    }
}

function play() {
    var audio = document.getElementById("myaudio");
    audio.volume = 0.3;
    audio.play();
}

function playvideo() {
    var video = document.getElementById("myvideo");
    video.setAttribute("src", "/Video/soitmm1.mp4");
    video.play();
}

document.addEventListener('click', function() {
    if (pressed == false) {
        pressed = true
        document.body.classList.add('blur-off');
        play();
        playvideo();
    } 
});
