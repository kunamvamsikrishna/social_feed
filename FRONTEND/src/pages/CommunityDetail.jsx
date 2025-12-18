import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { communitiesAPI, postsAPI } from '../services/api';
import { useAuth } from '../context/AuthContext';
import PostCard from '../components/PostCard';
import CreatePost from '../components/CreatePost';
import './CommunityDetail.css';

const CommunityDetail = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const { user } = useAuth();
  const [community, setCommunity] = useState(null);
  const [posts, setPosts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [showCreatePost, setShowCreatePost] = useState(false);

  useEffect(() => {
    loadCommunityData();
  }, [id]);

  const loadCommunityData = async () => {
    try {
      const communityRes = await communitiesAPI.getById(id);
      setCommunity(communityRes.data);
      
      // Only load posts if user is a member
      if (communityRes.data.is_member) {
        const postsRes = await postsAPI.getCommunityFeed(id);
        setPosts(postsRes.data.results);
      } else {
        setPosts([]);
      }
    } catch (err) {
      setError('Failed to load community');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleJoin = async () => {
    try {
      await communitiesAPI.join(id);
      loadCommunityData();
    } catch (err) {
      alert(err.response?.data?.message || 'Failed to join community');
    }
  };

  const handleLeave = async () => {
    if (!confirm('Are you sure you want to leave this community?')) return;
    
    try {
      await communitiesAPI.leave(id);
      navigate('/communities');
    } catch (err) {
      alert(err.response?.data?.error || 'Failed to leave community');
    }
  };

  const handlePostCreated = (newPost) => {
    setPosts([newPost, ...posts]);
    setShowCreatePost(false);
  };

  const handlePostDeleted = (postId) => {
    setPosts(posts.filter(p => p.id !== postId));
  };

  const handleLikeToggle = (postId, newLikeCount, isLiked) => {
    setPosts(posts.map(p => 
      p.id === postId 
        ? { ...p, like_count: newLikeCount, is_liked: isLiked }
        : p
    ));
  };

  if (loading) {
    return <div className="loading">Loading community...</div>;
  }

  if (error) {
    return <div className="error-page">{error}</div>;
  }

  if (!community) {
    return <div className="error-page">Community not found</div>;
  }

  return (
    <div className="community-detail-page">
      <div className="community-header-section">
        <div className="community-info">
          <button className="btn-back" onClick={() => navigate('/communities')}>
            ← Back to Communities
          </button>
          
          <h1>{community.name}</h1>
          <p className="community-desc">{community.description}</p>
          
          <div className="community-meta">
            <span>👥 {community.member_count} members</span>
            <span>📝 {community.post_count} posts</span>
            <span>Created by {community.created_by}</span>
          </div>

          {user && (
            <div className="community-actions-header">
              {community.is_member ? (
                <>
                  <button 
                    className="btn-primary"
                    onClick={() => setShowCreatePost(true)}
                  >
                    + Create Post
                  </button>
                  {community.created_by_id !== user.id && (
                    <button 
                      className="btn-secondary"
                      onClick={handleLeave}
                    >
                      Leave Community
                    </button>
                  )}
                </>
              ) : (
                <button 
                  className="btn-primary"
                  onClick={handleJoin}
                >
                  Join Community
                </button>
              )}
            </div>
          )}
        </div>
      </div>

      <div className="posts-section">
        <h2>Community Feed</h2>
        
        {!community.is_member ? (
          <div className="empty-posts">
            <h3>Join to see posts</h3>
            <p>You must be a member of this community to view and interact with posts.</p>
          </div>
        ) : posts.length === 0 ? (
          <div className="empty-posts">
            <h3>No posts yet</h3>
            <p>Be the first to post in this community!</p>
          </div>
        ) : (
          <div className="posts-list">
            {posts.map(post => (
              <PostCard
                key={post.id}
                post={post}
                onDelete={handlePostDeleted}
                onLikeToggle={handleLikeToggle}
                isMember={community.is_member}
              />
            ))}
          </div>
        )}
      </div>

      {showCreatePost && (
        <CreatePost
          communityId={community.id}
          communityName={community.name}
          onClose={() => setShowCreatePost(false)}
          onPostCreated={handlePostCreated}
        />
      )}
    </div>
  );
};

export default CommunityDetail;
