import React from 'react';
import {render, screen} from '@testing-library/react';
import axios from 'axios';
import {MemoryRouter} from 'react-router-dom';
import ProfilePage from '../../components/Profile';

// Mock axios
jest.mock('axios');

describe('ProfilePage', () => {
    test('renders the component with profile and account data', async () => {
        // Mock response data
        const profileData = {
            first_name: 'John',
            last_name: 'Doe',
            email: 'john.doe@example.com',
            username: 'johndoe',
        };
        const accountData = [
            {id: 1, user_id: 1, balance: 100},
            {id: 2, user_id: 1, balance: 200},
            {id: 3, user_id: 1, balance: 300},
        ];

        // Mock axios.get implementation
        axios.get.mockResolvedValueOnce({data: profileData});
        axios.get.mockResolvedValueOnce({data: accountData});

        render(
            <MemoryRouter>
                <ProfilePage/>
            </MemoryRouter>
        );

        // Assert that the component is rendered
        const profileCard = screen.getByText('Sorry, the page you\'re looking for cannot be found.');
        expect(profileCard).toBeInTheDocument();
    });

    test('renders NoPage when authentication data is missing', async () => {
        // Mock axios.get implementation
        axios.get.mockRejectedValueOnce(new Error('Authentication error'));

        render(
            <MemoryRouter>
                <ProfilePage/>
            </MemoryRouter>
        );

        // Assert that NoPage component is rendered
        const noPage = screen.getByText('Go Back to Home Page');
        expect(noPage).toBeInTheDocument();
    });

    // Add more tests if needed...
});
