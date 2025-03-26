import React, { useState, useEffect, useRef } from 'react';
import { motion } from 'framer-motion';

// Глобальный цвет для обычных (Card) кнопок
const GLOBAL_COLOR = '#2563eb';
const MAIN_CATEGORY_COLOR = ' #ae3be0';

/* 1. RandomAnimatedButton: 
   - Цвет кнопки (btnColor) выбирается случайно, если не передан через пропс.
   - Изначально текст чёрный, при клике (active) фон заполняется этим цветом и текст становится белым.
   - Анимация обводки рассчитывается динамически по периметру кнопки.
*/
export const RandomAnimatedButton = ({ children, type, active, color, ...props }) => {
    //const btnColor = type === 'main' ? MAIN_CATEGORY_COLOR : SUBCATEGORY_COLOR;
    const btnColor = MAIN_CATEGORY_COLOR
    return (
        <button
            className="relative px-2 py-1 md:px-4 md:py-2 rounded-xl font-semibold transition-colors duration-300"
            style={{
                backgroundColor: active ? btnColor : 'white',
                color: active ? 'black' : btnColor,
                border: `1px solid rgb(222, 222, 222)`,
            }}
            {...props}
        >
            {children}
        </button>
    );
};


/* 2. CardButton:
   - Простой вариант кнопки для карточек.
   - Использует глобальный цвет (или переданный через пропс) для рамки, текст остаётся чёрным.
*/
export const CardButton = ({ children, type, color, onClick, ...props }) => {
    const btnColor = type === 'first' ? true : false;
    const [copied, setCopied] = useState(false);

    const handleClick = async (e) => {
        if (type === 'first') {
            await onClick?.(e);
            setCopied(true);
            setTimeout(() => setCopied(false), 800);
        } else {
            onClick?.(e);
        }
    };

    return (
        <button
            onClick={handleClick}
            className={`px-2 py-1 md:px-2 md:py-1 rounded-xl font-semibold transition duration-300 transform ${copied ? 'scale-102 bg-[#ae3be0] text-white' : ''}`}
            style={{
                backgroundColor: btnColor && !copied ? 'white' : !copied ? `${MAIN_CATEGORY_COLOR}` : undefined,
                border: `1px solid ${MAIN_CATEGORY_COLOR}`,
                color: btnColor && !copied ? `${MAIN_CATEGORY_COLOR}` : "white",
            }}
            {...props}
        >
            {copied ? 'Copied!' : children}
        </button>
    );
};