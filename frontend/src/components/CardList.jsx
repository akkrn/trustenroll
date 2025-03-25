import React from 'react';
import { CardButton } from './ui/button';

export default function CardList({ groupedCards, isLoading }) {
    const handleCopy = (cardName) => {
        const number = cardName.split('|')[0].trim();
        navigator.clipboard.writeText(number);
    };

    if (isLoading) {
        return (
            <div className="flex justify-center items-center h-64">
                <div className="animate-spin rounded-full h-16 w-16 border-t-4 border-blue-500"></div>
            </div>
        );
    }

    return (
        <div className="w-full max-w-5xl mt-12 px-4 flex flex-col items-center">
            {groupedCards.map(({ bank_name, cards }) => (
                <div key={bank_name} className="mb-12 w-full">
                    <h2 className="text-lg sm:text-xl font-bold mb-2 text-center uppercase tracking-wide text-black-700">{bank_name}</h2>
                    <div className="flex flex-col gap-2">
                        {cards.map((card) => (
                            <div
                                key={card.id}
                                className="flex flex-col sm:flex-row justify-between items-center p-2 border-b border-gray-200 rounded-lg"
                            >
                                <span className="text-sm sm:text-base font-normal text-black-700">{card.card_name}</span>
                                <div className="flex gap-6 mt-1 sm:mt-0">
                                    <CardButton type="first" onClick={() => handleCopy(card.card_name)}>Copy #</CardButton>
                                    <a
                                        href={`https://t.me/TrustEnroll`}
                                        target="_blank"
                                        rel="noopener noreferrer"
                                    >
                                        <CardButton variant="outline">Buy</CardButton>
                                    </a>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            ))}
        </div>
    );
}