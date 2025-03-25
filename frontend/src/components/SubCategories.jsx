import React from 'react';
import { RandomAnimatedButton } from './ui/button';

export default function SubCategories({ subCategories, activeSubCategory, onSelectSubCategory }) {
    if (!subCategories.length) return null;

    return (
        <div className="flex flex-wrap justify-center gap-4 mt-4 px-4">
            {subCategories.map((sub) => (
                <RandomAnimatedButton
                    type="sub"
                    key={sub.id}
                    active={activeSubCategory === sub.id}
                    onClick={() => onSelectSubCategory(sub.id)}
                >
                    {sub.name}
                </RandomAnimatedButton>
            ))}
        </div>
    );
}