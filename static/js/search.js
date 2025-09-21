document.addEventListener("DOMContentLoaded", function () {
    function searchArticles() {
        let query = document.getElementById("search-box").value.toLowerCase();
        let articles = document.querySelectorAll(".article-container");

        articles.forEach(article => {
            let title = article.querySelector("h3").textContent.toLowerCase();

            if (title.includes(query)) {
                article.style.display = "block"; // Show matching articles
            } else {
                article.style.display = "none";  // Hide non-matching articles
            }
        });
    }

    // Attach event listener to search bar
    let searchBox = document.getElementById("search-box");
    if (searchBox) {
        searchBox.addEventListener("input", searchArticles);
    }
});
