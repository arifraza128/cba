import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../api";

function Profile() {
  const [data, setData] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    api.get('/profile')
      .then((response) => {
        setData(response.data);
        setIsLoading(false);
      })
      .catch(() => {
        localStorage.removeItem('token');
        navigate('/');
      });
  }, [navigate]);

  const logout = () => {
    localStorage.removeItem('token');
    navigate('/');
  };

  if (isLoading) {
    return (
      <div className="profile-container">
        <div className="loader-wrapper">
          <div className="pulse-loader"></div>
          <p>Retrieving secure session...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="profile-container">
      <div className="glass-card profile-card">
        <div className="card-header">
          <div className="avatar-glow">
            {data?.user?.username?.substring(0, 2).toUpperCase()}
          </div>
          <h2>User Profile</h2>
          <p className="subtitle">Secure session dashboard</p>
        </div>

        {data && (
          <div className="profile-details">
            <div className="welcome-banner">
              <h3>{data.message}</h3>
            </div>
            
            <div className="details-grid">
              <div className="detail-item">
                <span className="label">User Identifier</span>
                <span className="value">#{data.user.id}</span>
              </div>
              
              <div className="detail-item">
                <span className="label">Email Address</span>
                <span className="value">{data.user.email}</span>
              </div>
              
              <div className="detail-item">
                <span className="label">Username</span>
                <span className="value">{data.user.username}</span>
              </div>
            </div>
          </div>
        )}

        <div className="card-actions">
          <button onClick={logout} className="btn-secondary">
            Sign Out
          </button>
        </div>
      </div>
    </div>
  );
}

export default Profile;
