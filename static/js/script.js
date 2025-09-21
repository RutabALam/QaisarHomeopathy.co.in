let slideIndex = 0;

function showSlides() {
    let slides = document.getElementsByClassName("slide");

    if (slides.length === 0) {
        console.error("No slides found!");
        return;
    }

    // Hide all slides smoothly
    for (let i = 0; i < slides.length; i++) {
        slides[i].style.opacity = "0";
        slides[i].style.transition = "opacity 1.5s ease-in-out"; // Smooth fade effect
        slides[i].style.display = "none";
    }

    slideIndex++;

    if (slideIndex > slides.length) {
        slideIndex = 1;
    }

    // Show the next slide with a fade effect
    slides[slideIndex - 1].style.display = "block";
    setTimeout(() => {
        slides[slideIndex - 1].style.opacity = "1";
    }, 100); // Small delay for better transition

    setTimeout(showSlides, 7000); // Change slide every 5 seconds
}

// Manual slide change
function changeSlide(n) {
    slideIndex += n - 1;
    if (slideIndex < 0) {
        slideIndex = 0;
    }
    showSlides();
}

document.addEventListener("DOMContentLoaded", () => {
    showSlides();
});
