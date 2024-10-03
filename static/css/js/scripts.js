document.getElementById('movieForm').addEventListener('submit', function(event) {
    event.preventDefault();

    // Collect user input
    const genre = document.getElementById('genre').value;
    const story = document.getElementById('story').value;
    const actor = document.getElementById('actor').value;

    // Simulate movie recommendation (you will replace this with ML model integration)
    const recommendedMovie = recommendMovie(genre, story, actor);

    // Display the recommendation with animation
    const recommendationDiv = document.getElementById('recommendation');
    const movieNameP = document.getElementById('movieName');
    movieNameP.textContent = recommendedMovie;

    recommendationDiv.classList.add('show');
});

// Dummy function to simulate movie recommendation (replace this with backend API call)
function recommendMovie(genre, story, actor) {
    return "Inception";  // Replace this with actual ML recommendation from your model
}
