import React, {useState} from 'react';
import axios from "axios";
import {Button, Modal} from "react-bootstrap";

function setAuthExpiration(expirationTime) {
    const expiration = new Date();
    expiration.setMinutes(expiration.getMinutes() + expirationTime);
    localStorage.setItem('authExpiration', expiration.toISOString());
}

const SuccessRegisterPopup = ({show, handleClose}) => {
    return (
        <Modal show={show} onHide={handleClose}>
            <Modal.Header closeButton>
                <Modal.Title>Registration Successful</Modal.Title>
            </Modal.Header>
            <Modal.Body>
                <p>Your registration was successful!</p>
            </Modal.Body>
            <Modal.Footer>
                <Button variant="primary" onClick={handleClose}>
                    Close
                </Button>
            </Modal.Footer>
        </Modal>
    );
};

const FailPopup = ({show, handleClose, errorMessage}) => {
    return (
        <Modal show={show} onHide={handleClose}>
            <Modal.Header closeButton>
                <Modal.Title>Registration failed</Modal.Title>
            </Modal.Header>
            <Modal.Body>
                <p>An error occurred while trying to register:</p>
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

function RegisterForm() {
    const [fullname, setFullName] = useState('');
    const [email, setEmail] = useState('');
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [confirmPassword, setConfirmPassword] = useState('');
    const [isRegisterSuccessful, setIsRegisterSuccessful] = useState(false);
    const [errorMessage, setErrorMessage] = useState("");

    const handleCloseSuccess = () => {
        setIsRegisterSuccessful(false);
        window.location.reload();
    }

    const handleCloseError = () => setErrorMessage("");

    const handleRegister = async (event) => {
        event.preventDefault();

        const firstName = fullname.split(' ')[0];
        const lastName = fullname.split(' ')[1];
        const headers = {
            'Content-Type': 'application/json'
        };

        const data = {
            firstName,
            lastName,
            email,
            username,
            password
        };

        try {
            const response = await axios.post('http://localhost:8090/users', data, {headers});

            if (response.status === 200 || response.status === 201) {
                localStorage.setItem('authData', btoa(`${email}:${password}`));
                setAuthExpiration(5);
                const registerModal = document.getElementById('registerModal');
                registerModal.classList.remove('show');
                registerModal.setAttribute('aria-hidden', 'true');
                const modalBackdrop = document.getElementsByClassName('modal-backdrop')[0];
                modalBackdrop.parentNode.removeChild(modalBackdrop);
                document.body.classList.remove('modal-open');
                setIsRegisterSuccessful(true);
            } else {
                setErrorMessage(response.data.errors[0].message)
            }
        } catch (error) {
            setErrorMessage(`${error.response.data.errors[0].message}`);
        }
    };

    return (
        <div className="modal fade" id="registerModal" tabIndex="-1" role="dialog" aria-labelledby="registerModalLabel"
             aria-hidden="true">
            <div className="modal-dialog" role="document">
                <div className="modal-content">
                    <div className="modal-header">
                        <h5 className="modal-title" id="registerModalLabel">Register</h5>
                        <button type="button" className="close" data-dismiss="modal" aria-label="Close">
                            <span aria-hidden="true">&times;</span>
                        </button>
                    </div>
                    <div className="modal-body">
                        <form onSubmit={handleRegister}>
                            <div className="form-group">
                                <label htmlFor="registerName">Full name</label>
                                <input type="text" className="form-control" id="registerName"
                                       placeholder="Enter your full name"
                                       value={fullname}
                                       onChange={(event) => setFullName(event.target.value)}
                                />
                            </div>
                            <div className="form-group">
                                <label htmlFor="registerEmail">Email address</label>
                                <input type="email" className="form-control" id="registerEmail"
                                       aria-describedby="emailHelp"
                                       placeholder="Enter email"
                                       value={email}
                                       onChange={(event) => setEmail(event.target.value)}
                                />
                                <small id="emailHelp" className="form-text text-muted">We'll never share your
                                    email with anyone else.</small>
                            </div>
                            <div className="form-group">
                                <label htmlFor="registerUsername">Username</label>
                                <input type="text" className="form-control" id="registerUsername"
                                       placeholder="Enter username"
                                       value={username}
                                       onChange={(event) => setUsername(event.target.value)}
                                />
                            </div>
                            <div className="form-group">
                                <label htmlFor="registerPassword">Password</label>
                                <input type="password" className="form-control" id="registerPassword"
                                       placeholder="Password"
                                       value={password}
                                       onChange={(event) => setPassword(event.target.value)}
                                />
                            </div>
                            <div className="form-group">
                                <label htmlFor="registerConfirmPassword">Confirm Password</label>
                                <input type="password" className="form-control" id="registerConfirmPassword"
                                       placeholder="Confirm Password"
                                       value={confirmPassword}
                                       onChange={(event) => setConfirmPassword(event.target.value)}
                                />
                            </div>
                            <button type="submit" className="btn btn-primary">Submit</button>
                        </form>
                        <SuccessRegisterPopup show={isRegisterSuccessful} handleClose={handleCloseSuccess}/>
                        <FailPopup show={errorMessage !== ""} handleClose={handleCloseError}
                                   errorMessage={errorMessage}/>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default RegisterForm;
