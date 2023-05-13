import React, {useState} from 'react';
import "./../App.scss";

const ResetPasswordForm = () => {
    const [newPassword, setNewPassword] = useState('');
    const [confirmNewPassword, setConfirmNewPassword] = useState('');

    const handleSubmit = (e) => {
        e.preventDefault();

        const queryParams = new URLSearchParams(window.location.search);
        const token = queryParams.get('token');

        if (newPassword !== confirmNewPassword) {
            alert("Passwords don't match");
            return;
        }

        const requestData = new FormData();
        requestData.append('new_password', newPassword);
        requestData.append('confirm_password', confirmNewPassword);

        fetch(require('./../../package.json').config.BACKEND_URL + '/reset-password?token=' + token, {
            method: 'POST',
            body: requestData,
        })
            .then((response) => window.location.href = '/')
            .catch((error) => {
                alert(error);
            });
    };

    return (
        <div className="form-container">
            <form onSubmit={handleSubmit}>
                <input
                    type="password"
                    placeholder="New Password"
                    value={newPassword}
                    onChange={(e) => setNewPassword(e.target.value)}
                />
                <input
                    type="password"
                    placeholder="Confirm New Password"
                    value={confirmNewPassword}
                    onChange={(e) => setConfirmNewPassword(e.target.value)}
                />
                <button type="submit">Reset Password</button>
            </form>
        </div>
    );
};

export default ResetPasswordForm;
