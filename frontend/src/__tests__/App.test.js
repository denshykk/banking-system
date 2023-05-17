import React from 'react';
import { render, screen } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import App from '../App';

jest.mock('./../components/Header', () => () => <div data-testid="header">Header Component</div>);
jest.mock('./../components/Main', () => () => <div data-testid="main">Main Component</div>);
jest.mock('./../components/Footer', () => () => <div data-testid="footer">Footer Component</div>);
jest.mock('./../components/NoPage', () => () => <div data-testid="no-page">NoPage Component</div>);
jest.mock('./../components/Account', () => () => <div data-testid="account">Account Component</div>);
jest.mock('./../components/Profile', () => () => <div data-testid="profile">Profile Component</div>);

describe('App', () => {
  test('renders header', () => {
    render(<App />, { wrapper: MemoryRouter });
    const headerElement = screen.getByTestId('header');
    expect(headerElement).toBeInTheDocument();
  });

  test('renders main component for the home route', () => {
    render(
      <MemoryRouter initialEntries={['/']}>
        <App />
      </MemoryRouter>
    );
    const mainElement = screen.getByTestId('main');
    expect(mainElement).toBeInTheDocument();
  });

  test('renders footer', () => {
    render(<App />, { wrapper: MemoryRouter });
    const footerElement = screen.getByTestId('footer');
    expect(footerElement).toBeInTheDocument();
  });
});
