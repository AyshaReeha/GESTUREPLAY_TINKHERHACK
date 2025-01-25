// Fetch existing blog posts from localStorage or initialize an empty array
const posts = JSON.parse(localStorage.getItem('posts')) || [];

// Display posts on the homepage
function displayPosts() {
  const blogList = document.getElementById('blog-list');
  if (!blogList) return; // Exit if not on the homepage

  blogList.innerHTML = posts.map((post, index) => `
    <div class="blog-post">
      <h3>${post.title}</h3>
      <p>By ${post.author} | Category: ${post.category}</p>
      <button onclick="viewPost(${index})">Read More</button>
    </div>
  `).join('');
}

// Save a new post
function savePost(event) {
  event.preventDefault();

  const title = document.getElementById('title').value;
  const author = document.getElementById('author').value;
  const category = document.getElementById('category').value;
  const content = document.getElementById('content').value;

  posts.push({ title, author, category, content });
  localStorage.setItem('posts', JSON.stringify(posts));

  alert('Post saved successfully!');
  window.location.href = 'index.html';
}

// View a post
function viewPost(index) {
  localStorage.setItem('currentPost', JSON.stringify(posts[index]));
  window.location.href = 'post.html';
}

// Display post details
function displayPostDetails() {
  const post = JSON.parse(localStorage.getItem('currentPost'));
  if (!post) return;

  document.body.innerHTML = `
    <header>
      <h1>${post.title}</h1>
      <nav>
        <a href="index.html">Home</a>
      </nav>
    </header>
    <main>
      <p><strong>Author:</strong> ${post.author}</p>
      <p><strong>Category:</strong> ${post.category}</p>
      <article>${post.content}</article>
    </main>
    <footer>
      <p>&copy; 2025 Computer Science Association</p>
    </footer>
  `;
}

// Attach event listeners
document.getElementById('new-post-form')?.addEventListener('submit', savePost);
document.addEventListener('DOMContentLoaded', () => {
    // Run this only on the homepage (index.html)
    if (window.location.pathname === '/index.html') {
      displayPosts();
    }
  
    // Run this only on post.html
    if (window.location.pathname === '/post.html') {
      displayPostDetails();
    }
  });
  
