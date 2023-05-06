import React, {useState} from 'react';
import {Button, Modal} from "react-bootstrap";
import axios from "axios";

function setAuthExpiration(expirationTime) {
    const expiration = new Date();
    expiration.setMinutes(expiration.getMinutes() + expirationTime);
    localStorage.setItem('authExpiration', expiration.toISOString());
}

function LoginForm() {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [errorMessage, setErrorMessage] = useState('');

    const FailedLoginPopup = ({show, handleClose, errorMessage}) => {
        return (
            <Modal show={show} onHide={handleClose}>
                <Modal.Header closeButton>
                    <Modal.Title>Login failed</Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    <p>There was an error with your login:</p>
                    <p>{errorMessage}</p>
                </Modal.Body>
                <Modal.Footer>
                    <Button variant="primary" onClick={handleClose}>
                        Close
                    </Button>
                </Modal.Footer>
            </Modal>
        );
    };

    const handleCloseError = () => setErrorMessage('');

    const handleSubmit = async (event) => {
        event.preventDefault();

        const loginUrl = 'http://localhost:8090/users/login';
        const authData = btoa(`${email}:${password}`);
        const headers = {
            'Authorization': `Basic ${authData}`,
            'Content-Type': 'application/json'
        };

        try {
            const response = await axios.post(loginUrl, null, {
                headers: headers,
            });
            const data = response.data;

            if (response.status === 200) {
                localStorage.setItem('authData', authData);
                setAuthExpiration(5);
                const loginModal = document.getElementById('loginModal');
                loginModal.classList.remove('show');
                loginModal.setAttribute('aria-hidden', 'true');
                const modalBackdrop = document.getElementsByClassName('modal-backdrop')[0];
                modalBackdrop.parentNode.removeChild(modalBackdrop);
                document.body.classList.remove('modal-open');
                window.location.reload();
            } else {
                setErrorMessage(data.errors[0].message)
            }
        } catch (error) {
            setErrorMessage("Please verify correctness of your login and password!")
        }
    };

    return (
        <div className="modal fade" id="loginModal" tabIndex="-1" role="dialog" aria-labelledby="loginModalLabel"
             aria-hidden="true">
            <div className="modal-dialog" role="document">
                <div className="modal-content">
                    <div className="modal-header">
                        <h5 className="modal-title" id="loginModalLabel">Login</h5>
                        <button type="button" className="close" data-dismiss="modal" aria-label="Close">
                            <span aria-hidden="true">&times;</span>
                        </button>
                    </div>
                    <div className="modal-body">
                        <form onSubmit={handleSubmit}>
                            <div className="form-group">
                                <label htmlFor="loginEmail">Email address</label>
                                <input type="email" className="form-control" id="loginEmail"
                                       aria-describedby="emailHelp"
                                       placeholder="Enter email"
                                       value={email}
                                       onChange={(event) => setEmail(event.target.value)}
                                />
                                <small id="emailHelp" className="form-text text-muted">We'll never share your
                                    email with anyone else.</small>
                            </div>
                            <div className="form-group">
                                <label htmlFor="loginPassword">Password</label>
                                <input type="password" className="form-control" id="loginPassword"
                                       placeholder="Password"
                                       value={password}
                                       onChange={(event) => setPassword(event.target.value)}
                                />
                            </div>
                            <button type="submit" className="btn btn-primary">Submit</button>
                        </form>
                        <FailedLoginPopup show={errorMessage !== ''} handleClose={handleCloseError}
                                          errorMessage={errorMessage}/>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default LoginForm;
