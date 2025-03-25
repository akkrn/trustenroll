import React from 'react';
import header from '../assets/header.jpg';

export default function Header() {
    return (
        <div className="relative h-full overflow-hidden">
            <a href="/"><img
                src={header}
                alt="Header Background"
                className="w-full object-bottom h-full object-cover"
            /></a>
        </div>
    );
}