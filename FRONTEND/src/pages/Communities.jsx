import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { communitiesAPI } from '../services/api';
import { useAuth } from '../context/AuthContext';
import './Communities.css';

const Communities = () => {
  const navigate = useNavigate();
  const { user } = useAuth();
  const [communities, setCommunities] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [newCommunity, setNewCommunity] = useState({ name: '', description: '' });
  const [creating, setCreating] = useState(false);

  useEffect(() => {
    loadCommunities();
  }, []);

  const loadCommunities = async () => {
    try {
      const response = await communitiesAPI.getAll();
      setCommunities(response.data.results);
    } catch (err) {
      setError('Failed to load communities');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleCreateCommunity = async (e) => {
    e.preventDefault();
    setCreating(true);

    try {
      const response = await communitiesAPI.create(newCommunity);
      setCommunities([response.data, ...communities]);
      setShowCreateModal(false);
      setNewCommunity({ name: '', description: '' });
    } catch (err) {
      alert(err.response?.data?.name?.[0] || 'Failed to create community');
    } finally {
      setCreating(false);
    }
  };

  const handleJoinCommunity = async (communityId) => {
    try {
      await communitiesAPI.join(communityId);
      loadCommunities(); // Reload to update is_member status
    } catch (err) {
      alert(err.response?.data?.message || 'Failed to join community');
    }
  };

  if (loading) {
    return <div className="loading">Loading communities...</div>;
  }

  return (
    <div className="communities-page">
      <div className="communities-header">
        <div>
          <h1>Communities</h1>
          <p>Discover and join communities</p>
        </div>
        {user && (
          <button 
            className="btn-primary"
            onClick={() => setShowCreateModal(true)}
          >
            + Create Community
          </button>
        )}
      </div>

      {error && <div className="error-message">{error}</div>}

      <div className="communities-grid">
        {communities.map((community) => (
          <div key={community.id} className="community-card">
            <div className="community-card-header">
              <h3>{community.name}</h3>
              {community.is_member && (
                <span className="badge-member">Member</span>
              )}
            </div>
            
            <p className="community-description">{community.description}</p>
            
            <div className="community-stats">
              <span>👥 {community.member_count} members</span>
              <span>📝 {community.post_count} posts</span>
            </div>

            <div className="community-actions">
              <button 
                className="btn-secondary"
                onClick={() => navigate(`/communities/${community.id}`)}
              >
                View Community
              </button>
              
              {user && !community.is_member && (
                <button 
                  className="btn-primary"
                  onClick={() => handleJoinCommunity(community.id)}
                >
                  Join
                </button>
              )}
            </div>
          </div>
        ))}
      </div>

      {communities.length === 0 && (
        <div className="empty-state">
          <h3>No communities yet</h3>
          <p>Be the first to create one!</p>
        </div>
      )}

      {showCreateModal && (
        <div className="modal-overlay" onClick={() => setShowCreateModal(false)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <h2>Create Community</h2>
            <form onSubmit={handleCreateCommunity}>
              <div className="form-group">
                <label>Community Name</label>
                <input
                  type="text"
                  value={newCommunity.name}
                  onChange={(e) => setNewCommunity({ ...newCommunity, name: e.target.value })}
                  required
                  autoFocus
                />
              </div>

              <div className="form-group">
                <label>Description</label>
                <textarea
                  value={newCommunity.description}
                  onChange={(e) => setNewCommunity({ ...newCommunity, description: e.target.value })}
                  rows="4"
                  required
                />
              </div>

              <div className="modal-actions">
                <button 
                  type="button" 
                  className="btn-secondary"
                  onClick={() => setShowCreateModal(false)}
                >
                  Cancel
                </button>
                <button type="submit" className="btn-primary" disabled={creating}>
                  {creating ? 'Creating...' : 'Create'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default Communities;
