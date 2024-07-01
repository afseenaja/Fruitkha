window.onscroll = function() { scrollFunction() };

function scrollFunction() {
    const topRow = document.getElementById("topRow");

    // Change background color when scrolling
    if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
        topRow.style.backgroundColor = "black";
    } else {
        topRow.style.backgroundColor = "transparent";
    }
}
// search window

function toggleSearch() {
  var newDiv = document.getElementById('new');
  if (newDiv.style.visibility === "hidden") {
      newDiv.style.visibility = "visible";
  } else {
      newDiv.style.visibility = "hidden";
  }
}

// time index.html
var countDownDate = new Date("Jan 1, 2024 12:00:00").getTime();

// Update the count down every 1 second
var x = setInterval(function() {

  // Get today's date and time
  var now = new Date().getTime();
    
  // Find the distance between now and the count down date
  var distance = countDownDate - now;
    
  // Time calculations for days, hours, minutes and seconds
  var days = Math.floor(distance / (1000 * 60 * 60 * 24));
  var hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
  var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
  var seconds = Math.floor((distance % (1000 * 60)) / 1000);
    
  // Output the result in an element with id="demo"
  document.getElementById("day").innerHTML = days;
  document.getElementById('hour').innerHTML=hours;
  document.getElementById('min').innerHTML=minutes;
  document.getElementById('sec').innerHTML=seconds; 
  // If the count down is over, write some text 
  if (distance < 0) {
    clearInterval(x);
    document.getElementById('day').innerHTML="00";
    document.getElementById('hour').innerHTML="00";
    document.getElementById('min').innerHTML="00";
    document.getElementById('sec').innerHTML="00";
  }
}, 1000);
// setInterval(clock, 1000)
// function clock(){
//   var today=new Date();
//   var d=today.getDay();
//   var h=today.getHours();
//   var m=today.getMinutes();
//   var s=today.getSeconds();
//   document.getElementById('day').innerHTML="0"+d;
//   document.getElementById('hour').innerHTML=h;
//   document.getElementById('min').innerHTML=m;
//   document.getElementById('sec').innerHTML=s;
// }
// clock();
// shop.html active button

function filterSelection(filter, button) {
  const cards = document.querySelectorAll('.row3 .card');

  // Remove active class from all buttons
  document.querySelectorAll('.nav-link').forEach(btn => {
    btn.classList.remove('active');
  });

  // Add active class to the clicked button
  button.classList.add('active');

  cards.forEach(card => {
    const fruitType = card.id.toLowerCase();
    const showCard = filter === 'All' || fruitType.includes(filter.toLowerCase());
    
    // Set the display property to 'inline-block' for filtered cards
    card.style.display = showCard ? 'inline-block' : 'none';
  });
}
// function filterSelection(filter, button) {
//   const cards = document.querySelectorAll('.row3 .card');

//   // Remove active class from all buttons
//   document.querySelectorAll('.nav-link').forEach(btn => {
//     btn.classList.remove('active');
//   });

//   // Add active class to the clicked button
//   button.classList.add('active');

//   cards.forEach(card => {
//     const fruitType = card.id.toLowerCase();
//     const showCard = filter === 'All' || fruitType.includes(filter.toLowerCase());
    
//     // Set the display property to 'inline-block' for filtered cards
//     card.style.display = showCard ? 'inline-block' : 'none';
//   });
// }


// document.addEventListener('DOMContentLoaded', function () {
//   // Initial page load, show all products
//   filterSelection('All', document.querySelector('.nav-link.active'));
// });

// function filterSelection(filter, button) {
//   const cards = document.querySelectorAll('.row3 .card');

//   // Remove active class from all buttons
//   document.querySelectorAll('.nav-link').forEach(btn => {
//     btn.classList.remove('active');
//   });

//   // Add active class to the clicked button
//   button.classList.add('active');

//   cards.forEach(card => {
//     const fruitType = card.id.toLowerCase();
//     const showCard = filter === 'All' || fruitType.includes(filter.toLowerCase());
//     card.style.display = showCard ? 'block' : 'none';
//   });
// }


// checkout.html

let currentContent = null;

function toggleContent(contentId) {
  const contentElement = document.getElementById(contentId);

  if (currentContent) {
    // Hide the previously displayed content
    currentContent.style.display = 'none';
  }

  if (currentContent !== contentElement) {
    // Show the clicked content if it's not already displayed
    contentElement.style.display = 'table';
    currentContent = contentElement;
  } else {
    // If the same button is clicked again, hide the content
    currentContent = null;
  }
  if(contentId=='shipping'|| contentId=='card'){
    var x=document.getElementById('billing');
    x.style.display="none"
  }
}

// let currentContent = null;

// function toggleContent(contentId) {
//   const contentElement = document.getElementById(contentId);

//   if (currentContent === contentElement) {
//     // If the same button is clicked again, hide the content
//     contentElement.style.display = 'none';
//     currentContent = null;
//   } else {
//     // Hide the currently displayed content (if any)
//     if (currentContent) {
//       currentContent.style.display = 'none';
//     }

//     // Show the clicked content
//     contentElement.style.display = 'table';
//     currentContent = contentElement;
//   }
// }
