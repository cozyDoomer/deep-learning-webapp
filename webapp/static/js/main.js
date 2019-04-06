// setTimeout() function will be fired after page is loaded
// it will wait for 5 sec. and then will fire
// $(".message_flash").hide() function
$(document).ready(function() {
    setTimeout(function() {
        $(".message_flash").animate({ opacity: 0 })
    }, 5000);
})   

$(document).ready(function() {
    $('#contactForm').submit(function () {
        sendContactForm();
        return false;
    });
})

// Modal Image Gallery
function onClick(element) {
    document.getElementById("img01").src = element.src;
    document.getElementById("modal01").style.display = "block";
    var captionText = document.getElementById("caption");
    captionText.innerHTML = element.alt;
}


// Used to toggle the menu on small screens when clicking on the menu button
function toggleFunction() {
    var x = document.getElementById("navDemo");
    if (x.className.indexOf("show") == -1) {
        x.className += " show";
    } else {
        x.className = x.className.replace(" show", "");
    }
}