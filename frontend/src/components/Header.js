import React from 'react';
import {useState, useEffect} from 'react';
import "./../App.scss";
import Transfer from "./Transfer";
import {Link, useHistory} from "react-router-dom";
import Account from "./Account";

function Header() {
    const history = useHistory();
    const [isLoggedIn, setIsLoggedIn] = useState(false);

    useEffect(() => {
        const authData = localStorage.getItem('authData');
        const authExpiration = localStorage.getItem('authExpiration');

        if (authData && authExpiration) {
            const expirationDate = new Date(authExpiration);

            if (new Date() < expirationDate) {
                setIsLoggedIn(true);
            } else {
                localStorage.removeItem('authData');
                localStorage.removeItem('authExpiration');
            }
        }
    }, []);

    const handleLogout = () => {
        localStorage.removeItem('authData');
        localStorage.removeItem('authExpiration');
        history.push("/");
        window.location.reload();
    };

    return (
        <header>
            <nav className="navbar navbar-expand-md navbar-light">
                <div className="container">
                    <Link to="/" className="navbar-brand">Banking System</Link>
                    <button className="navbar-toggler" type="button" data-toggle="collapse"
                            data-target="#navbarCollapse"
                            aria-controls="navbarCollapse" aria-expanded="false" aria-label="Toggle navigation">
                        <span className="navbar-toggler-icon"></span>
                    </button>
                    <div className="collapse navbar-collapse" id="navbarCollapse">
                        <ul className="navbar-nav ml-auto">
                            {isLoggedIn ? (
                                    <>
                                        <li className="nav-item">
                                            <Link to="/accounts" className="nav-link" href="#" id="admin-btn"
                                                  click={<Account/>}>Accounts</Link>
                                        </li>
                                        <li className="nav-item">
                                            <Link to="/transfer" className="nav-link" href="#" id="admin-btn"
                                                  click={<Transfer/>}>Transfer</Link>
                                        </li>
                                        <li className="nav-item">
                                            <Link to="/" className="nav-link" href="#" id="logout-btn"
                                                  onClick={handleLogout}>Logout</Link>
                                        </li>
                                    </>
                                ) :
                                (
                                    <>
                                        <li className="nav-item">
                                            <Link to="/" className="nav-link" href="#" id="register-btn"
                                                  data-toggle="modal"
                                                  data-target="#registerModal">Register</Link>
                                        </li>
                                        <li className="nav-item">
                                            <Link to="/" className="nav-link" href="#" id="login-btn"
                                                  data-toggle="modal"
                                                  data-target="#loginModal">Login</Link>
                                        </li>
                                    </>
                                )
                            }
                        </ul>
                    </div>
                </div>
            </nav>
        </header>
    );
}

export default Header;
