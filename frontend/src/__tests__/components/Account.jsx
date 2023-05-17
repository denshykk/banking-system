import React from 'react';
import {render, fireEvent, waitFor, act, getAllByText, findAllByText, queryAllByText} from '@testing-library/react';
import axios from 'axios';
import Account from './../../components/Account';

jest.mock('axios');

describe('Account', () => {
    afterEach(() => {
        jest.clearAllMocks();
        localStorage.clear();
    });

    test('should render "You have no accounts" message when no accounts are present', async () => {
        axios.get.mockResolvedValueOnce({data: []});

        localStorage.setItem('authExpiration', '2023-05-15T12:00:00.000Z');
        localStorage.setItem('authData', 'mockAuthToken');

        const {getByText} = render(<Account/>);

        await waitFor(() => {
            const noAccountsMessage = getByText('You have no accounts.');

            expect(noAccountsMessage).toBeInTheDocument();
        });
    });

    test('should create an account when "Create Account" button is clicked', async () => {
        axios.post.mockResolvedValueOnce({});

        localStorage.setItem('authExpiration', '2023-05-15T12:00:00.000Z');
        localStorage.setItem('authData', 'mockAuthToken');

        const {getByText} = render(<Account/>);

        const createAccountButton = getByText('Create Account');
        act(() => {
            fireEvent.click(createAccountButton);
        });

        await waitFor(() => {
            expect(axios.post).toHaveBeenCalledTimes(1);
            expect(axios.post).toHaveBeenCalledWith(
                expect.stringContaining('/accounts'),
                null,
                {
                    headers: {
                        Authorization: expect.stringContaining('mockAuthToken'),
                    },
                }
            );
        });
    });
});
