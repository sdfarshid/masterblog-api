let currentPage = 1;  // Default page
let totalPages = 1;   // Will be updated based on response
let perPage = 3;      // PerPage
let isSearchMode = false; //

// Function that runs once the window is fully loaded
window.onload = function() {
    // Attempt to retrieve the API base URL from the local storage
    var savedBaseUrl = localStorage.getItem('apiBaseUrl');
    // If a base URL is found in local storage, load the posts
    if (savedBaseUrl) {
        document.getElementById('api-base-url').value = savedBaseUrl;
        loadPosts();
    }

}


// Function to fetch all the posts from the API and display them on the page
function loadPosts(posts = null) {
    if (posts) {
        renderPosts(posts);
        return;
    }

    // Retrieve the base URL from the input field and save it to local storage
    var baseUrl = document.getElementById('api-base-url').value;
    let perPage = document.getElementById('post-per_page').value;
    let sortField = document.getElementById('sort-field').value;
    let direction = document.getElementById('sort-direction').value;
    localStorage.setItem('apiBaseUrl', baseUrl);
    isSearchMode = false;
    // Use the Fetch API to send a GET request to the /posts endpoint
    let queryString = `?per_page=${perPage}&sort=${sortField}&direction=${direction}&page=${currentPage}`;

    fetch(baseUrl + '/posts' + queryString)
        .then(response => response.json())  // Parse the JSON data from the response
        .then(data => {  // Once the data is ready, we can use it
           // Assuming the response contains pagination info like total pages
            totalPages = Math.ceil(data.total / perPage); // Update total pages

            // For each post in the response, create a new post element and add it to the page
            renderPosts(data.posts);

            // Assuming the response contains pagination info like total pages

            updatePagination();

        })
        .catch(error => console.error('Error:', error));  // If an error occurs, log it to the console
}

function renderPosts(posts) {
    const postContainer = document.getElementById('post-container');
    postContainer.innerHTML = ''; // Clear previous posts

    posts.forEach(post => {
        const postDiv = document.createElement('div');
        postDiv.className = 'post';
        postDiv.innerHTML = `
            <h2>${post.title}</h2>
            <p>${post.content}</p>
            <span>${post.author} : </span>
            <span>${post.date}</span>
            <button onclick="deletePost(${post.id})">Delete</button>`;
        postContainer.appendChild(postDiv);
    });
}

function updatePagination() {
    if (isSearchMode) {
        document.getElementById('pagination').style.display = 'none';
        return;
    }
    document.getElementById('pagination').style.display = 'block';

    const paginationContainer = document.getElementById('pagination');
    paginationContainer.innerHTML = '';  // Clear previous pagination buttons

    // Create "Previous" button
    if (currentPage > 1) {
        const prevButton = document.createElement('button');
        prevButton.textContent = 'Previous';
        prevButton.onclick = () => {
            currentPage--;
            loadPosts();
        };
        paginationContainer.appendChild(prevButton);
    }

    // Create "Next" button
    if (currentPage < totalPages) {
        const nextButton = document.createElement('button');
        nextButton.textContent = 'Next';
        nextButton.onclick = () => {
            currentPage++;
            loadPosts();
        };
        paginationContainer.appendChild(nextButton);
    }
}



// Function to send a POST request to the API to add a new post
function addPost() {
    // Retrieve the values from the input fields
    var baseUrl = document.getElementById('api-base-url').value;
    var postTitle = document.getElementById('post-title').value;
    var postContent = document.getElementById('post-content').value;
    var postAuthor = document.getElementById('post-author').value;
    var postDate = document.getElementById('post-date').value;

    // Use the Fetch API to send a POST request to the /posts endpoint
    fetch(baseUrl + '/posts', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title: postTitle, content: postContent, author: postAuthor, date: postDate })
    })
    .then(response => response.json())  // Parse the JSON data from the response
    .then(post => {
        console.log('Post added:', post);
        loadPosts(); // Reload the posts after adding a new one
    })
    .catch(error => console.error('Error:', error));  // If an error occurs, log it to the console
}

// Function to send a POST request to the API to add a new post
function searchPost() {
    // Retrieve the values from the input fields
    var baseUrl = document.getElementById('api-base-url').value;
    var postTitle = document.getElementById('search-post-title').value;
    var postContent = document.getElementById('search-post-content').value;
    var postAuthor = document.getElementById('search-post-author').value;
    var postDate = document.getElementById('search-post-date').value;

    // Use the Fetch API to send a POST request to the /posts endpoint
  let queryString = `?title=${postTitle}&content=${postContent}&author=${postAuthor}&date=${postDate}`;
    fetch(baseUrl + '/posts/search' + queryString)
        .then(response => response.json())
        .then(data => {
            isSearchMode = true; //
            renderPosts(data); // Render search results
            document.getElementById('pagination').style.display = 'none';

        })
        .catch(error => console.error('Error:', error));
}

// Function to send a DELETE request to the API to delete a post
function deletePost(postId) {
    var baseUrl = document.getElementById('api-base-url').value;

    // Use the Fetch API to send a DELETE request to the specific post's endpoint
    fetch(baseUrl + '/posts/' + postId, {
        method: 'DELETE'
    })
    .then(response => {
        console.log('Post deleted:', postId);
        loadPosts(); // Reload the posts after deleting one
    })
    .catch(error => console.error('Error:', error));  // If an error occurs, log it to the console
}
