import React from 'react';
import {render} from '@testing-library/react';
import Footer from './../../components/Footer';

describe('Footer', () => {
    it('should render the contact information', () => {
        const {getByText} = render(<Footer/>);

        expect(getByText('Contact Us')).toBeInTheDocument();
        expect(getByText('123 Main St')).toBeInTheDocument();
        expect(getByText('Anytown, USA')).toBeInTheDocument();
        expect(getByText('555-123-4567')).toBeInTheDocument();
    });

    it('should render the social media icons', () => {
        const getByLabelText = render(<Footer/>);

        expect(getByLabelText.container.getElementsByClassName('fab fa-facebook-f')).not.toBeNull();
        expect(getByLabelText.container.getElementsByClassName('fab fa-twitter')).not.toBeNull();
        expect(getByLabelText.container.getElementsByClassName('fab fa-instagram')).not.toBeNull();
    });

    it('should render the visit hours', () => {
        const {getByText} = render(<Footer/>);

        expect(getByText('Visit Us')).toBeInTheDocument();
        expect(getByText('Monday - Friday: 9:00am - 5:00pm')).toBeInTheDocument();
        expect(getByText('Saturday: 10:00am - 2:00pm')).toBeInTheDocument();
        expect(getByText('Sunday: Closed')).toBeInTheDocument();
    });

    it('should render the copyright notice', () => {
        const {getByText} = render(<Footer/>);

        expect(getByText('© 2023 Banking System. All rights reserved.')).toBeInTheDocument();
    });
});
