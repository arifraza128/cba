import React, { useEffect, useState } from 'react';

function Posts() {
  const [posts, setPosts] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const getPosts = async () => {
      try {
        const response = await fetch('https://jsonplaceholder.typicode.com/posts');

        if (!response.ok) {
          throw new Error('Failed to fetch posts');
        }

        const data = await response.json();
        setPosts(data);
      } catch (error) {
        console.error(error);
      } finally {
        setLoading(false);
      }
    };

    getPosts();
  }, []);

  return (
    <div>
      <h2>Posts</h2>

      {loading ? (
        <p>Loading posts...</p>
      ) : (
        posts.map((post) => (
          <p key={post.id}>
            {post.id} - {post.title} - {post.body}
          </p>
        ))
      )}
    </div>
  );
}

export default Posts;
