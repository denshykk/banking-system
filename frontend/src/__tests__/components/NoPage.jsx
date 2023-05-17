import React from 'react';
import {render, screen} from '@testing-library/react';
import {BrowserRouter} from 'react-router-dom';
import NoPage from './../../components/NoPage';

describe('NoPage', () => {
    test('renders the component', () => {
        render(
            <BrowserRouter>
                <NoPage/>
            </BrowserRouter>
        );

        // Assert that the component is rendered
        const pageTitle = screen.getByText('404');
        expect(pageTitle).toBeInTheDocument();

        const pageContent = screen.getByText(
            "Sorry, the page you're looking for cannot be found."
        );
        expect(pageContent).toBeInTheDocument();
    });

    test('renders a link to the home page', () => {
        render(
            <BrowserRouter>
                <NoPage/>
            </BrowserRouter>
        );

        // Assert that the link is rendered with the correct text and href
        const link = screen.getByRole('link', {name: 'Go Back to Home Page'});
        expect(link).toBeInTheDocument();
        expect(link.getAttribute('href')).toBe('/');
    });

    // Add more tests if needed...
});
