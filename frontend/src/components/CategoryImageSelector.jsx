import React, { useState } from 'react';

export default function CategoryImageSelector({ onSelect }) {
    const [active, setActive] = useState(null); // теперь null — обе неактивны

    const handleSelect = (category) => {
        const newValue = active === category ? null : category;
        setActive(newValue);
        onSelect(newValue); // передаём null, если клик повторный
    };

    return (
        <div className="flex flex-wrap justify-center gap-4 py-4">
            {/* Debit */}
            <img
                src="/images/debit.jpg"
                alt="Debit"
                onClick={() => handleSelect('debit')}
                className={`h-full w-[20rem]  rounded-lg cursor-pointer transition duration-300 object-cover ${active === 'debit' ? '' : 'grayscale'
                    }`}
            />

            {/* Credit */}
            <img
                src="/images/credit.jpg"
                alt="Credit"
                onClick={() => handleSelect('credit')}
                className={`h-full w-[20rem] rounded-lg cursor-pointer transition duration-300 object-cover  ${active === 'credit' ? '' : 'grayscale'
                    }`}
            />

            {/* NFC */}
            <img
                src="/images/nfc.jpg"
                alt="NFC"
                onClick={() => handleSelect('nfc')}
                className={`h-full w-[20rem] rounded-lg cursor-pointer transition duration-300 object-cover  ${active === 'nfc' ? '' : 'grayscale'
                    }`}
            />
        </div>
    );
}
