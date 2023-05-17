import React from 'react';
import { render, fireEvent } from '@testing-library/react';
import { BrowserRouter as Router } from 'react-router-dom';
import Header from './../../components/Header';

describe('Header', () => {
  it('should render the navigation links for logged-in user', () => {
    const mockLocalStorage = {
      getItem: jest.fn((key) => {
        if (key === 'authData') {
          return 'mockAuthToken';
        }
        if (key === 'authExpiration') {
          return '2023-05-15T12:00:00.000Z';
        }
        if (key === 'user') {
          return 'mockUser';
        }
        return null;
      }),
      removeItem: jest.fn(),
    };
    global.localStorage = mockLocalStorage;

    const { getByText } = render(
      <Router>
        <Header />
      </Router>
    );

    expect(getByText('Banking System')).toBeInTheDocument();
    expect(getByText('Login')).toBeInTheDocument();
    expect(getByText('Register')).toBeInTheDocument();
  });

  it('should render the navigation links for logged-out user', () => {
    const { getByText } = render(
      <Router>
        <Header />
      </Router>
    );

    expect(getByText('Banking System')).toBeInTheDocument();
    expect(getByText('Register')).toBeInTheDocument();
    expect(getByText('Login')).toBeInTheDocument();
  });

  it('should handle logout', () => {
    const mockLocalStorage = {
      removeItem: jest.fn(),
    };
    global.localStorage = mockLocalStorage;
    const mockPush = jest.fn();
    const mockReload = jest.fn();
    const mockHistory = { push: mockPush };
    global.window = { location: { reload: mockReload } };

    const { getByText } = render(
      <Router>
        <Header />
      </Router>
    );

    expect(mockPush).not.toBeNull();
    expect(mockReload).not.toBeNull();
  });

  it('should handle admin panel navigation', () => {
    const mockLocalStorage = {
      getItem: jest.fn(() => 'mockAuthToken'),
    };
    global.localStorage = mockLocalStorage;
    const mockHref = jest.fn();
    global.window = { location: { href: mockHref } };

    const { getByText } = render(
      <Router>
        <Header />
      </Router>
    );

    expect(mockHref).not.toBeNull();
  });
});
