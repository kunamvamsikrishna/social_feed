import { useState } from 'react';
import { postsAPI } from '../services/api';
import { useAuth } from '../context/AuthContext';
import './PostCard.css';

const PostCard = ({ post, onDelete, onLikeToggle }) => {
  const { user } = useAuth();
  const [isDeleting, setIsDeleting] = useState(false);

  const handleLike = async () => {
    try {
      const response = await postsAPI.toggleLike(post.id);
      onLikeToggle(post.id, response.data.like_count, response.data.is_liked);
    } catch (err) {
      console.error('Failed to toggle like:', err);
      if (err.response?.status === 403) {
        alert('You must be a member of this community to like posts');
      }
    }
  };

  const handleDelete = async () => {
    if (!confirm('Are you sure you want to delete this post?')) return;
    
    setIsDeleting(true);
    try {
      await postsAPI.delete(post.id);
      onDelete(post.id);
    } catch (err) {
      alert('Failed to delete post');
      setIsDeleting(false);
    }
  };

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    const now = new Date();
    const diffMs = now - date;
    const diffMins = Math.floor(diffMs / 60000);
    const diffHours = Math.floor(diffMs / 3600000);
    const diffDays = Math.floor(diffMs / 86400000);

    if (diffMins < 1) return 'Just now';
    if (diffMins < 60) return `${diffMins}m ago`;
    if (diffHours < 24) return `${diffHours}h ago`;
    if (diffDays < 7) return `${diffDays}d ago`;
    return date.toLocaleDateString();
  };

  return (
    <div className="post-card">
      <div className="post-header">
        <div className="post-author-info">
          <div className="author-avatar">
            {post.author.first_name[0]}{post.author.last_name[0]}
          </div>
          <div>
            <div className="author-name">
              {post.author.first_name} {post.author.last_name}
            </div>
            <div className="post-time">{formatDate(post.created_at)}</div>
          </div>
        </div>
        
        {user && user.id === post.author.id && (
          <button 
            className="btn-delete"
            onClick={handleDelete}
            disabled={isDeleting}
          >
            🗑️
          </button>
        )}
      </div>

      <div className="post-content">
        {post.content}
      </div>

      <div className="post-actions">
        <button 
          className={`btn-like ${post.is_liked ? 'liked' : ''}`}
          onClick={handleLike}
          disabled={!user}
        >
          {post.is_liked ? '❤️' : '🤍'} {post.like_count}
        </button>
      </div>
    </div>
  );
};

export default PostCard;
