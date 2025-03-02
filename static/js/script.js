document.addEventListener("DOMContentLoaded", () => {
    const sidebar = document.getElementById("sidebar");
    const toggleSidebar = document.getElementById("toggleSidebar");
    const contentDiv = document.getElementById("content");
    const topicButtons = document.querySelectorAll(".topic-btn");

    // Sidebar Toggle (Prevent errors if the button is missing)
    if (toggleSidebar) {
        toggleSidebar.addEventListener("click", () => {
            sidebar.classList.toggle("-translate-x-full");
        });
    }

    // Change Content on Click
    topicButtons.forEach(button => {
        button.addEventListener("click", () => {
            const topicId = button.getAttribute("data-topic");
            fetch(`/topic/${topicId}`)
                .then(response => {
                    if (!response.ok) throw new Error("Грешка при зареждането");
                    return response.json();
                })
                .then(data => {
                    contentDiv.innerHTML = `<h2 class="text-2xl font-bold">${data.title}</h2><p>${data.content}</p>`;
                })
                .catch(error => console.error(error));
        });
    });
});
