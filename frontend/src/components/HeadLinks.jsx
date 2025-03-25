import React, { useState } from 'react';
import { Menu, X } from 'lucide-react';
import { Send } from 'lucide-react'; // или любая другая иконка телеги

const links = [
    { label: 'How to buy', href: "https://telegra.ph/Base-info-01-24" },
    { label: 'FAQ', href: "https://telegra.ph/Enroll-FAQ-03-21" },
    { label: 'NFC FAQ', href: "https://telegra.ph/NFC-GUIDE-03-20" },
    { label: 'Vouches', href: "https://t.me/TrustEnrollVouches" },
    { label: 'SSN Search BOT', href: "https://t.me/TrustFinderTwo_bot" },
    { label: 'WWH Forum', href: "https://wwh-club.to/index.php?threads/trust-enroll-kachestvennyj-i-unikalnyj-enroll-material.267552/" },
    { label: 'Channel with updates', href: "https://t.me/+QSk1AwmqC4RkNTVi" },
    { label: 'Support', href: "https://t.me/TrustEnroll" },
];

export default function HeaderLinks() {
    const [open, setOpen] = useState(false);

    const mainLinks = links.slice(0, -2);
    const specialLinks = links.slice(-2);

    return (
        <div className="w-full bg-white py-2">
            {/* Desktop */}
            <div className="hidden md:flex flex-row justify-center items-center w-full px-8 py-2 gap-4">

                {/* Main Links */}
                <div className="flex justify-center gap-4">
                    {mainLinks.map(({ label, href }, index) => (
                        <React.Fragment key={label}>
                            <a
                                href={href}
                                className="custom-font font-medium text-gray-700 hover:text-blue-600 transition-colors duration-200"
                            >
                                {label}
                            </a>
                            {index < mainLinks.length - 1 && (
                                <span className="text-gray-400 hidden sm:inline">|</span>
                            )}
                        </React.Fragment>
                    ))}
                </div>

                {/* Special Buttons */}
                <div className="flex gap-4">
                    {specialLinks.map(({ label, href }, idx) => (
                        <a
                            key={label}
                            href={href}
                            target="_blank"
                            rel="noopener noreferrer"
                            className={`flex items-center gap-2 px-4 py-2 rounded-xl font-semibold text-white duration-300 ${idx === 0
                                ? 'bg-gradient-to-r from-blue-500 to-blue-700'
                                : 'bg-gradient-to-r from-pink-500 to-pink-700'
                                }`}
                        >
                            <Send size={18} />
                            {label}
                        </a>
                    ))}
                </div>

            </div>

            {/* Mobile */}
            <div className="flex md:hidden justify-center">
                <button onClick={() => setOpen(!open)} className="p-2">
                    {open ? <X size={24} color="#ae3be0" /> : <Menu size={24} color="#ae3be0" />}
                </button>
            </div>

            {open && (
                <div className="flex flex-col md:hidden items-center gap-2 mt-2">
                    {mainLinks.map(({ label, href }) => (
                        <a
                            key={label}
                            href={href}
                            className="custom-font font-medium text-gray-700"
                        >
                            {label}
                        </a>
                    ))}
                    <div className="flex flex-col items-center text-center gap-2 w-full px-4 mt-2">
                        {specialLinks.map(({ label, href }, idx) => (
                            <a
                                key={label}
                                href={href}
                                target="_blank"
                                rel="noopener noreferrer"
                                className={`flex justify-center items-center gap-2 px-4 py-2 rounded-xl font-semibold text-white w-1/2 ${idx === 0
                                    ? 'bg-gradient-to-r from-blue-500 to-blue-700'
                                    : 'bg-gradient-to-r from-pink-500 to-pink-700'
                                    }`}
                            >
                                <Send size={18} />
                                {label}
                            </a>
                        ))}
                    </div>
                </div>
            )}
        </div>
    );
}