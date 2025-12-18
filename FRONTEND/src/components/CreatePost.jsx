import { useState } from 'react';
import { postsAPI } from '../services/api';
import './CreatePost.css';

const CreatePost = ({ communityId, communityName, onClose, onPostCreated }) => {
  const [content, setContent] = useState('');
  const [creating, setCreating] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (content.trim().length === 0) {
      setError('Post content cannot be empty');
      return;
    }

    setCreating(true);
    setError('');

    try {
      const response = await postsAPI.create({
        content: content.trim(),
        community: communityId
      });
      setContent('');
      setCreating(false);
      onPostCreated(response.data);
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to create post');
      setCreating(false);
    }
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <h2>Create Post</h2>
        <p className="modal-subtitle">Posting in {communityName}</p>

        {error && <div className="error-message">{error}</div>}

        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label>What's on your mind?</label>
            <textarea
              value={content}
              onChange={(e) => setContent(e.target.value)}
              placeholder="Share your thoughts..."
              rows="6"
              autoFocus
              maxLength="5000"
            />
            <div className="char-count">
              {content.length}/5000
            </div>
          </div>

          <div className="modal-actions">
            <button 
              type="button" 
              className="btn-secondary"
              onClick={onClose}
              disabled={creating}
            >
              Cancel
            </button>
            <button 
              type="submit" 
              className="btn-primary"
              disabled={creating || content.trim().length === 0}
            >
              {creating ? 'Posting...' : 'Post'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default CreatePost;
