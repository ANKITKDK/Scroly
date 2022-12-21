// Slider 1 Starts
let thumbnails1 = document.getElementsByClassName('abc');
let slider = document.getElementById('slider1');
const maxScrollLeft = slider.scrollWidth - slider.clientWidth;
function autoPlay() {
    if (slider.scrollLeft > (maxScrollLeft - 1)) {
        slider.scrollLeft -= maxScrollLeft;
    } else {
        slider.scrollLeft += 1;
    }
}
let play = setInterval(autoPlay, 30);
for (var i=0; i < thumbnails1.length; i++){  
thumbnails1[i].addEventListener('mouseover', function() {
    clearInterval(play);
});
thumbnails1[i].addEventListener('mouseout', function() {
    return play = setInterval(autoPlay, 30);
});
}



//Slider 2 Starts
let thumbnails2= document.getElementsByClassName('abc2');
let slider2 = document.getElementById('slider2');
console.log(thumbnails2.length)
console.log(slider)
const maxScrollLeft2 = slider2.scrollWidth - slider2.clientWidth;
function autoPlay2() {
    if (slider2.scrollLeft > (maxScrollLeft2 - 1)) {
        slider2.scrollLeft -= maxScrollLeft2;
    } else {
        slider2.scrollLeft += 1;
    }
}
let play2 = setInterval(autoPlay2, 30);
for (var i=0; i < thumbnails1.length; i++){  
thumbnails2[i].addEventListener('mouseover', function() {
    clearInterval(play2);
});
thumbnails2[i].addEventListener('mouseout', function() {
    return play2 = setInterval(autoPlay2, 30);
});
}


//Slider 3 Starts
let thumbnails3= document.getElementsByClassName('abc3');
let slider3 = document.getElementById('slider3');
console.log(thumbnails3.length)
console.log(slider)
const maxScrollLeft3 = slider3.scrollWidth - slider3.clientWidth;
function autoPlay3() {
    if (slider3.scrollLeft > (maxScrollLeft3 - 1)) {
        slider3.scrollLeft -= maxScrollLeft3;
    } else {
        slider3.scrollLeft += 1;
    }
}
let play3 = setInterval(autoPlay3, 30);
for (var i=0; i < thumbnails1.length; i++){  
thumbnails3[i].addEventListener('mouseover', function() {
    clearInterval(play3);
});
thumbnails3[i].addEventListener('mouseout', function() {
    return play3 = setInterval(autoPlay3, 30);
});
}


//Slider 4 Starts
let thumbnails4= document.getElementsByClassName('abc4');
let slider4 = document.getElementById('slider4');
console.log(thumbnails3.length)
console.log(slider)
const maxScrollLeft4 = slider3.scrollWidth - slider3.clientWidth;
function autoPlay4() {
    if (slider4.scrollLeft > (maxScrollLeft4 - 1)) {
        slider4.scrollLeft -= maxScrollLeft4;
    } else {
        slider4.scrollLeft += 1;
    }
}
let play4 = setInterval(autoPlay4, 30);
for (var i=0; i < thumbnails1.length; i++){  
thumbnails4[i].addEventListener('mouseover', function() {
    clearInterval(play4);
});
thumbnails4[i].addEventListener('mouseout', function() {
    return play4 = setInterval(autoPlay4, 30);
});
}