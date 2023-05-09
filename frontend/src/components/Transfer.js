import React, {useState} from "react";
import NoPage from "./NoPage";
import {Button, Modal} from "react-bootstrap";

const SuccessTransferPopup = ({show, handleClose}) => {
    return (
        <Modal show={show} onHide={handleClose}>
            <Modal.Header closeButton>
                <Modal.Title>Transfer Successful</Modal.Title>
            </Modal.Header>
            <Modal.Body>
                <p>Your transfer was successful!</p>
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
                <Modal.Title>Transfer failed</Modal.Title>
            </Modal.Header>
            <Modal.Body>
                <p>There was an error with your transfer:</p>
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

function Transfer() {
    const [fromAcc, setFromAcc] = useState(0);
    const [toAcc, setToAcc] = useState(0);
    const [amount, setAmount] = useState(0.0);
    const [isTransferSuccessful, setIsTransferSuccessful] = useState(false);
    const [errorMessage, setErrorMessage] = useState("");

    const handleCloseSuccess = () => setIsTransferSuccessful(false);
    const handleCloseError = () => setErrorMessage("");

    const handleSubmit = async (event) => {
        event.preventDefault();

        const response = await fetch(`http://localhost:8090/accounts/${fromAcc}/transfer-to/${toAcc}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Basic ' + localStorage.getItem('authData')
            },
            body: JSON.stringify({
                amount: amount
            })
        });

        const data = await response.json();

        if (response.ok) {
            setIsTransferSuccessful(true);
        } else {
            setErrorMessage(data.errors[0].message);
        }
    };

    if (!(localStorage.getItem('authExpiration') && localStorage.getItem('authData'))) {
        return <NoPage/>
    }

    return (
        <div className="container" id="transfer">
            <h1>Transfer Money</h1>
            <hr/>
            <div className="row">
                <div className="col-md-6 offset-md-3">
                    <form onSubmit={handleSubmit}>
                        <div className="form-group">
                            <label htmlFor="fromAcc">Enter Source Account</label>
                            <input type="number" className="form-control" id="fromAcc"
                                   placeholder="12345"
                                   value={fromAcc}
                                   onChange={(event) => setFromAcc(event.target.value)}/>
                        </div>
                        <div className="form-group">
                            <label htmlFor="toAcc">Enter Target Account</label>
                            <input type="number" className="form-control" id="toAcc"
                                   placeholder="54321"
                                   value={toAcc}
                                   onChange={(event) => setToAcc(event.target.value)}/>
                        </div>
                        <div className="form-group">
                            <label htmlFor="amount">Amount</label>
                            <input type="number" className="form-control" id="amount"
                                   placeholder="Enter amount"
                                   value={amount}
                                   onChange={(event) => setAmount(event.target.value)}/>
                        </div>
                        <button type="submit" className="btn btn-primary">Transfer</button>
                    </form>
                    <SuccessTransferPopup show={isTransferSuccessful} handleClose={handleCloseSuccess}/>
                    <FailPopup show={errorMessage !== ""} handleClose={handleCloseError} errorMessage={errorMessage}/>
                </div>
            </div>
        </div>
    )
}

export default Transfer;
