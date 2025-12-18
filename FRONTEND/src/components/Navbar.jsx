import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import './Navbar.css';

const Navbar = () => {
  const { user, logout, isAuthenticated } = useAuth();
  const navigate = useNavigate();

  const handleLogout = async () => {
    await logout();
    navigate('/login');
  };

  return (
    <nav className="navbar">
      <div className="navbar-content">
        <Link to="/communities" className="navbar-brand">
          🌐 Social Feed
        </Link>

        <div className="navbar-menu">
          {isAuthenticated ? (
            <>
              <Link to="/communities" className="nav-link">
                Communities
              </Link>
              <div className="user-menu">
                <div className="user-avatar">
                  {user?.first_name[0]}{user?.last_name[0]}
                </div>
                <span className="user-name">{user?.username}</span>
                <button onClick={handleLogout} className="btn-logout">
                  Logout
                </button>
              </div>
            </>
          ) : (
            <>
              <Link to="/communities" className="nav-link">
                Browse Communities
              </Link>
              <Link to="/login" className="btn-nav-login">
                Login
              </Link>
              <Link to="/register" className="btn-nav-register">
                Register
              </Link>
            </>
          )}
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
