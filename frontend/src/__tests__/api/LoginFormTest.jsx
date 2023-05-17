import React from 'react';
import {render, fireEvent, waitFor, screen} from '@testing-library/react';
import axios from 'axios';
import LoginForm from './../../api/LoginForm';

jest.mock('axios');

describe('LoginForm', () => {
    beforeEach(() => {
        jest.clearAllMocks();
    });

    test('renders LoginForm component', () => {
        render(<LoginForm/>);
        expect(screen.getByLabelText('Email address')).toBeInTheDocument();
        expect(screen.getByLabelText('Password')).toBeInTheDocument();
    });

    test('handles form submission successfully', async () => {
        const mockResponse = {
            status: 200,
            data: {
                errors: [],
            },
        };

        axios.post.mockResolvedValue(mockResponse);

        render(<LoginForm/>);

        const emailInput = screen.getByLabelText('Email address');
        const passwordInput = screen.getByLabelText('Password');
        const submitButton = screen.getByText('Submit');

        fireEvent.change(emailInput, {target: {value: 'test@example.com'}});
        fireEvent.change(passwordInput, {target: {value: 'password123'}});
        fireEvent.click(submitButton);

        await waitFor(() => {
            expect(axios.post).toHaveBeenCalledTimes(1);
            expect(axios.post).toHaveBeenCalledWith(
                expect.stringContaining('/users/login'),
                null,
                {
                    headers: {
                        Authorization: expect.stringContaining('Basic'),
                        'Content-Type': 'application/json',
                    },
                }
            );
        });
        expect(localStorage.getItem('authData')).toBeNull();
        expect(localStorage.getItem('user')).toBeNull();
    });

    test('displays forgot password form', () => {
        render(<LoginForm/>);
        const forgotPasswordButton = screen.getByText('Forgot Password?');
        fireEvent.click(forgotPasswordButton);
        expect(screen.getByLabelText('Email address')).toBeInTheDocument();
        expect(screen.getByText('Back to Login')).toBeInTheDocument();
    });

    test('handles forgot password form submission', async () => {
        const mockResponse = {
            status: 200,
        };
        const alertMock = jest.spyOn(window, 'alert').mockImplementation();

        axios.post.mockResolvedValue(mockResponse);

        render(<LoginForm/>);

        const forgotPasswordButton = screen.getByText('Forgot Password?');
        fireEvent.click(forgotPasswordButton);

        const emailInput = screen.getByLabelText('Email address');
        const submitButton = screen.getByText('Submit');

        fireEvent.change(emailInput, {target: {value: 'test@example.com'}});
        fireEvent.click(submitButton);

        await waitFor(() => {
                expect(axios.post).toHaveBeenCalledTimes(1);
                expect(axios.post).toHaveBeenCalledWith(
                    expect.stringContaining('/forgot-password'),
                    {email: 'test@example.com'},
                    {
                        headers: {
                            'Content-Type': 'multipart/form-data',
                        },
                    }
                );
            }
        );
        expect(alertMock).toHaveBeenCalledTimes(1);
    });

    test('handles forgot password form submission failure', async () => {
        const mockResponse = {
            status: 500,
        };
        const alertMock = jest.spyOn(window, 'alert').mockImplementation();
        axios.post.mockRejectedValue(mockResponse);

        render(<LoginForm/>);

        const forgotPasswordButton = screen.getByText('Forgot Password?');
        fireEvent.click(forgotPasswordButton);

        const emailInput = screen.getByLabelText('Email address');
        const submitButton = screen.getByText('Submit');

        fireEvent.change(emailInput, {target: {value: 'test@example.com'}});
        fireEvent.click(submitButton);

        await waitFor(() => {
            expect(axios.post).toHaveBeenCalledTimes(1);
        });
        expect(alertMock).toHaveBeenCalledTimes(1);
    });

    test('closes error popup on close button click', () => {
        render(<LoginForm/>);
        const closeButton = screen.getByText('×');
        fireEvent.click(closeButton);
        expect(screen.queryByText('Login failed')).toBeNull();
    });

    test('switches back to login form', () => {
        render(<LoginForm/>);
        const forgotPasswordButton = screen.getByText('Forgot Password?');
        fireEvent.click(forgotPasswordButton);
        const backButton = screen.getByText('Back to Login');
        fireEvent.click(backButton);
        expect(screen.getByLabelText('Email address')).toBeInTheDocument();
        expect(screen.getByLabelText('Password')).toBeInTheDocument();
    });
});
