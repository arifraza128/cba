import React, { useEffect, useState } from "react";
import api from "../api";


function Profile() {
  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(true);


  useEffect(() => {
    const fetchProfile = async () => {
      try {
        const response = await api.get("/profile");
        setProfile(response.data);
      } catch (error) {
        console.error("Error fetching profile:", error);
      } finally {
        setLoading(false);
      }
    };


    fetchProfile();
  }, []);


  if (loading) {
    return <h2>Loading profile...</h2>;
  }


  return (
    <div>
      <h1>Profile</h1>


      {profile && (
        <div>
          <p>Name: {profile.name}</p>
          <p>Email: {profile.email}</p>
        </div>
      )}
    </div>
  );
}


export default Profile;
