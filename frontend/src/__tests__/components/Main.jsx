import React from 'react';
import {render} from '@testing-library/react';
import Main from './../../components/Main';

describe('Main', () => {
    it('should render the about us section', () => {
        const {getByText} = render(<Main/>);
        expect(getByText('About Us')).toBeInTheDocument();
    });

    it('should render the accounts section', () => {
        const {getByText} = render(<Main/>);
        expect(getByText('Accounts')).toBeInTheDocument();
    });

    it('should render the loans section', () => {
        const {getByText} = render(<Main/>);
        expect(getByText('Loans')).toBeInTheDocument();
    });

    it('should render the investments section', () => {
        const {getByText} = render(<Main/>);
        expect(getByText('Investments')).toBeInTheDocument();
    });

});
