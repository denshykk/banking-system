import React from 'react';
import "./../App.scss";
import LoginForm from "../api/LoginForm";
import RegisterForm from "../api/RegisterForm";

function Main() {
    return (
        <main>
            <div className="container">
                <div className="row mt-5">
                    <div className="col-md-12">
                        <h2>About Us</h2>
                        <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed vitae ante ante. Nullam a
                            ultrices
                            sapien. Fusce auctor varius semper. Integer vitae velit mi. Proin consectetur enim nec diam
                            rhoncus
                            finibus. Praesent eget lectus consequat, hendrerit tortor eu, sodales quam. Integer non
                            luctus elit.
                            Integer in odio in nisl faucibus blandit. Proin sit amet lectus eu mauris malesuada feugiat.
                            Morbi
                            accumsan sodales nunc, sed mollis enim pharetra vitae. Etiam sodales augue sed arcu dapibus
                            malesuada. Donec auctor ex id augue rhoncus, vel tincidunt tortor tempus. Fusce at
                            vestibulum
                            nisl.</p>
                    </div>
                </div>
                <div className="row justify-content-center">
                    <div className="col-md-4">
                        <div className="card">
                            <div className="card-body">
                                <i className="fas fa-wallet fa-3x mb-3"></i>
                                <h3 className="card-title mb-3">Accounts</h3>
                                <p className="card-text">We offer a variety of checking and savings accounts to meet
                                    your financial
                                    needs. Whether you're just starting out or looking for a high-yield account, we have
                                    you
                                    covered.</p>
                                <a href="#" className="btn btn-primary">Learn More</a>
                            </div>
                        </div>
                    </div>
                    <div className="col-md-4">
                        <div className="card">
                            <div className="card-body">
                                <i className="fas fa-file-invoice-dollar fa-3x mb-3"></i>
                                <h3 className="card-title mb-3">Loans</h3>
                                <p className="card-text">Our loan options include personal loans, home loans, and auto
                                    loans. We
                                    offer competitive rates and flexible terms to meet your needs any time and place
                                    that suits
                                    you.</p>
                                <a href="#" className="btn btn-primary">Learn More</a>
                            </div>
                        </div>
                    </div>
                    <div className="col-md-4">
                        <div className="card">
                            <div className="card-body">
                                <i className="fas fa-chart-line fa-3x mb-3"></i>
                                <h3 className="card-title mb-3">Investments</h3>
                                <p className="card-text">We offer a range of investment options including mutual funds,
                                    stocks, and
                                    bonds. Our investment experts can help you create a portfolio that meets your
                                    financial
                                    goals.</p>
                                <a href="#" className="btn btn-primary">Learn More</a>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <RegisterForm/>
            <LoginForm/>
        </main>
    );
}

export default Main;
