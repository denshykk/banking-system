import React from 'react';
import "./../App.scss";

function Footer() {
    return (
        <footer className="mt-auto">
            <div className="container">
                <div className="row">
                    <div className="col-md-4">
                        <h3>Contact Us</h3>
                        <ul className="list-unstyled">
                            <li>123 Main St</li>
                            <li>Anytown, USA</li>
                            <li>555-123-4567</li>
                        </ul>
                    </div>
                    <div className="col-md-4">
                        <h3>Follow Us</h3>
                        <ul className="list-inline social-icons">
                            <li className="list-inline-item"><a href="#"><i className="fab fa-facebook-f"></i></a></li>
                            <li className="list-inline-item"><a href="#"><i className="fab fa-twitter"></i></a></li>
                            <li className="list-inline-item"><a href="#"><i className="fab fa-instagram"></i></a></li>
                        </ul>
                    </div>
                    <div className="col-md-4">
                        <h3>Visit Us</h3>
                        <ul className="list-unstyled">
                            <li>Monday - Friday: 9:00am - 5:00pm</li>
                            <li>Saturday: 10:00am - 2:00pm</li>
                            <li>Sunday: Closed</li>
                        </ul>
                    </div>
                </div>
                <div className="row">
                    <div className="col-md-12">
                        <p className="text-muted">© 2023 Banking System. All rights reserved.</p>
                    </div>
                </div>
            </div>
        </footer>
    )
}

export default Footer;
