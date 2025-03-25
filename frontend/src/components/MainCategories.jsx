import React from 'react';
import { RandomAnimatedButton } from './ui/button';

export default function MainCategories({ categories, activeCategory, onSelectCategory }) {
  return (
    <div className="flex flex-wrap justify-center gap-4 mt-8 px-4">
      {categories.map((cat) => (
        <RandomAnimatedButton
          type="main"
          key={cat.id}
          active={activeCategory === cat.id}
          onClick={() => onSelectCategory(cat.id)}
        >
          {cat.name}
        </RandomAnimatedButton>
      ))}
    </div>
  );
}