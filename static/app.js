document.addEventListener("DOMContentLoaded", function() {
    // Select all navigation links in the navbar
    const links = document.querySelectorAll("nav ul li a");

    // Add click event listener to each navigation link
    for (const link of links) {
        link.addEventListener("click", function(event) {
            // Prevent default link behavior (jumping to anchor)
            event.preventDefault();
            // Get the ID of the target section from the href attribute
            const targetId = this.getAttribute("href").substring(1);
            // Find the target section element by ID
            const targetElement = document.getElementById(targetId);

            // Smoothly scroll to the target section
            window.scrollTo({
                top: targetElement.offsetTop,
                behavior: "smooth"
            });

            // Manually activate the clicked link
            activateNavLink(this);
        });
    }

    // Function to add the active class to the current nav link
    function activateNavLink(activeLink) {
        links.forEach(link => link.classList.remove("active"));
        activeLink.classList.add("active");
    }

    // Select the comment form
    const form = document.querySelector("#comment-form form");
    // Add submit event listener to the form
    form.addEventListener("submit", function(event) {
        // Prevent default form submission
        event.preventDefault();

        // Create a FormData object from the form
        const formData = new FormData(form);
        // Extract form field values
        const name = formData.get("name");
        const email = formData.get("email");
        const comment = formData.get("comment");

        // Add the new comment to the comments list
        addComment(name, email, comment);

        // Alert the user that the form has been submitted successfully
        alert("Form submitted successfully!");
        // Reset the form fields
        form.reset();
    });

    // Function to add a new comment to the comments list
    function addComment(name, email, comment) {
        // Get the comments list container
        const commentsList = document.getElementById("comments-list");
        // Create a new div element for the comment
        const commentElement = document.createElement("div");
        commentElement.className = "comment";

        // Create a div for the comment header (name and email)
        const commentHeader = document.createElement("div");
        commentHeader.className = "comment-header";
        commentHeader.textContent = `${name} (${email})`;

        // Create a div for the comment body (comment text)
        const commentBody = document.createElement("div");
        commentBody.className = "comment-body";
        commentBody.textContent = comment;

        // Append the header and body to the comment element
        commentElement.appendChild(commentHeader);
        commentElement.appendChild(commentBody);
        // Append the comment element to the comments list
        commentsList.appendChild(commentElement);
    }

    // Add active class to navigation items on scroll
    const sections = document.querySelectorAll("section");
    const navItems = document.querySelectorAll("nav ul li a");

    const observerOptions = {
        root: null,
        rootMargin: "0px",
        threshold: 0.6 // Adjust the threshold as needed
    };

    const observerCallback = (entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const sectionId = entry.target.getAttribute("id");
                const navItem = document.querySelector(`nav ul li a[href="#${sectionId}"]`);

                if (navItem) {
                    activateNavLink(navItem);
                }
            }
        });
    };

    const observer = new IntersectionObserver(observerCallback, observerOptions);

    sections.forEach(section => {
        observer.observe(section);
    });
});
