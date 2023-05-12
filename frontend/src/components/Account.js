import React, {useEffect, useState} from 'react';
import axios from 'axios';
import NoPage from "./NoPage";

const Account = () => {
    const [accounts, setAccounts] = useState([]);

    const createAccount = async () => {
        try {
            await axios.post(require('./../../package.json').config.BACKEND_URL + '/accounts', null, {
                headers: {
                    Authorization: `Basic ${localStorage.getItem('authData')}`,
                },
            });
        } catch (error) {
            console.log(error);
        }
    };

    const deleteAccount = async (accountId) => {
        try {
            await axios.delete(require('./../../package.json').config.BACKEND_URL + `/accounts/${accountId}`, {
                headers: {
                    Authorization: `Basic ${localStorage.getItem('authData')}`,
                },
            });
        } catch (error) {
            console.log(error);
        }
    };

    const getAccounts = async () => {
        const token = localStorage.getItem('authData');
        try {
            const response = await axios.get(require('./../../package.json').config.BACKEND_URL + '/users/accounts', {
                headers: {
                    Authorization: `Basic ${token}`,
                },
            });
            setAccounts(response.data);
        } catch (error) {
            console.log(error);
        }
    };

    useEffect(() => {
        getAccounts();
    }, []);

    if (!(localStorage.getItem('authExpiration') && localStorage.getItem('authData'))) {
        return <NoPage/>
    }

    return (
        <div className="accountList">
            {accounts.length > 0 ? (
                <table className="table">
                    <thead>
                    <tr>
                        <th>Account ID</th>
                        <th>Balance</th>
                        <th></th>
                    </tr>
                    </thead>
                    <tbody>
                    {accounts.map((account) => (
                        <tr key={account.id}>
                            <td>{account.id}</td>
                            <td>{account.balance}</td>
                            <td>
                                <button className="btn btn-primary" id="deleteButton"
                                        onClick={() => deleteAccount(account.id)}>Delete
                                </button>
                            </td>
                        </tr>
                    ))}
                    </tbody>
                </table>
            ) : (
                <p>You have no accounts.</p>
            )}
            <button className="btn btn-primary" id="createAccount" onClick={createAccount}>Create Account</button>
        </div>
    );
};

export default Account;
