import React, {useEffect, useState} from 'react';
import axios from 'axios';
import "./../App.scss";
import NoPage from "./NoPage";

const ProfilePage = () => {
    const [profileData, setProfileData] = useState({});
    const [accountData, setAccountData] = useState([]);

    useEffect(() => {
        const fetchProfileData = async () => {
            try {
                const response = await axios.get(require('./../../package.json').config.BACKEND_URL + '/users',
                    {
                        headers: {
                            'Authorization': `Basic ${localStorage.getItem('authData')}`
                        }
                    });
                setProfileData(response.data);
            } catch (error) {
                console.error('Error fetching profile data:', error);
            }
        };

        const fetchAccountData = async () => {
            try {
                const response = await axios.get(require('./../../package.json').config.BACKEND_URL + '/users/accounts',
                    {
                        headers: {
                            'Authorization': `Basic ${localStorage.getItem('authData')}`
                        }
                    });
                setAccountData(response.data);
            } catch (error) {
                console.error('Error fetching profile data:', error);
            }
        };

        fetchProfileData();
        fetchAccountData();
    }, []);

    if (!(localStorage.getItem('authExpiration') && localStorage.getItem('authData'))) {
        return <NoPage/>
    }

    return (
        <div className="profile-container">
            <div className="profile-card">
                <h2>{profileData.first_name} {profileData.last_name}</h2>
                <p>Email: <span className="email">{profileData.email}</span></p>
                <p>Username: <span className="username">{profileData.username}</span></p>
                <p>Overall Balance: <span>${
                    accountData.map(({balance, id, user_id}) => balance)
                    .map((it) => Number(it))
                    .reduce((partialSum, a) => partialSum + a, 0)
                }</span></p>
            </div>
        </div>
    );
}

export default ProfilePage;
