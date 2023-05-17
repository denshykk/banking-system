import React from 'react';
import {render, fireEvent, waitFor} from '@testing-library/react';
import axios from 'axios';
import RegisterForm from './../../api/RegisterForm';

jest.mock('axios'); // Mock axios module

describe('RegisterForm', () => {
    test('should render the form correctly', () => {
        const {getByLabelText, getByText} = render(<RegisterForm/>);

        expect(getByLabelText('Full name')).toBeInTheDocument();
        expect(getByLabelText('Email address')).toBeInTheDocument();
        expect(getByLabelText('Username')).toBeInTheDocument();
        expect(getByLabelText('Password')).toBeInTheDocument();
        expect(getByLabelText('Confirm Password')).toBeInTheDocument();
        expect(getByText('Submit')).toBeInTheDocument();
    });

    test('should update form state when input fields change', () => {
        const {getByLabelText} = render(<RegisterForm/>);

        const fullnameInput = getByLabelText('Full name');
        const emailInput = getByLabelText('Email address');
        const usernameInput = getByLabelText('Username');
        const passwordInput = getByLabelText('Password');
        const confirmPasswordInput = getByLabelText('Confirm Password');

        fireEvent.change(fullnameInput, {target: {value: 'John Doe'}});
        fireEvent.change(emailInput, {target: {value: 'john.doe@example.com'}});
        fireEvent.change(usernameInput, {target: {value: 'johndoe'}});
        fireEvent.change(passwordInput, {target: {value: 'password123'}});
        fireEvent.change(confirmPasswordInput, {target: {value: 'password123'}});

        expect(fullnameInput.value).toBe('John Doe');
        expect(emailInput.value).toBe('john.doe@example.com');
        expect(usernameInput.value).toBe('johndoe');
        expect(passwordInput.value).toBe('password123');
        expect(confirmPasswordInput.value).toBe('password123');
    });

    test('should submit the form successfully', async () => {
        const {getByLabelText, getByText} = render(<RegisterForm/>);

        const fullnameInput = getByLabelText('Full name');
        const emailInput = getByLabelText('Email address');
        const usernameInput = getByLabelText('Username');
        const passwordInput = getByLabelText('Password');
        const confirmPasswordInput = getByLabelText('Confirm Password');
        const submitButton = getByText('Submit');

        fireEvent.change(fullnameInput, {target: {value: 'John Doe'}});
        fireEvent.change(emailInput, {target: {value: 'john.doe@example.com'}});
        fireEvent.change(usernameInput, {target: {value: 'johndoe'}});
        fireEvent.change(passwordInput, {target: {value: 'password123'}});
        fireEvent.change(confirmPasswordInput, {target: {value: 'password123'}});

        axios.post.mockResolvedValueOnce({
            status: 201, data: {
                "errors": [{
                    "message": "ERROR"
                }]
            }
        }); // Mock successful response

        fireEvent.click(submitButton);

        await waitFor(() => {
            expect(axios.post).toHaveBeenCalledTimes(1);
            expect(localStorage.getItem('authData')).not.toBeNull();
            expect(localStorage.getItem('user')).not.toBeNull();
        });
    });
});
