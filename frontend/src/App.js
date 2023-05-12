import React from 'react';
import "./App.scss";
import { BrowserRouter, Switch, Route } from 'react-router-dom';
import Header from './components/Header';
import Main from './components/Main';
import Footer from './components/Footer';
import Transfer from "./components/Transfer";
import NoPage from "./components/NoPage";
import Account from "./components/Account";

function App() {
    return (
        <BrowserRouter>
            <Header/>
            <Switch>
                <Route exact path="/" component={Main}/>
                <Route path="/transfer" component={Transfer}/>
                <Route path="/accounts" component={Account}/>
                <Route path="*" component={NoPage}/>
            </Switch>
            <Footer/>
        </BrowserRouter>
    );
}

export default App;
