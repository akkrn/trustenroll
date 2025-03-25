import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import Header from '../components/Header';
import MainCategories from '../components/MainCategories';
import SubCategories from '../components/SubCategories';
import CardList from '../components/CardList';
import HeaderLinks from '../components/HeadLinks';
import CategoryImageSelector from '../components/CategoryImageSelector';
import noCardsImg from '../assets/no-cards.png';

const API = process.env.REACT_APP_API;

export default function CardsPage() {
    const [mainCategories, setMainCategories] = useState([]);
    const [subCategories, setSubCategories] = useState([]);
    const [groupedCards, setGroupedCards] = useState([]);
    const [activeMainCategory, setActiveMainCategory] = useState(null);
    const [activeSubCategory, setActiveSubCategory] = useState(null);
    const [isLoading, setIsLoading] = useState(false);

    const cardsSectionRef = useRef(null);

    const groupCardsByBank = (cardsArray) => {
        const grouped = {};
        cardsArray.forEach(card => {
            const bankName = card.bank_name;
            if (!grouped[bankName]) {
                grouped[bankName] = [];
            }
            grouped[bankName].push(card);
        });

        return Object.entries(grouped).map(([bank_name, cards]) => ({
            bank_name,
            cards
        }));
    };

    useEffect(() => {
        const fetchInitialData = async () => {
            try {
                const [categoriesRes] = await Promise.all([
                    axios.get(`${API}/main_categories`),
                ]);
                setMainCategories(categoriesRes.data);
            } catch (error) {
                console.error('Ошибка при инициализации данных:', error);
            }
        };

        fetchInitialData();
    }, []);

    useEffect(() => {
        const fetchData = async () => {
            if (!activeMainCategory) {
                setSubCategories([]);
                setActiveSubCategory(null);
                setIsLoading(true);
                try {
                    const res = await axios.get(`${API}/all_cards`);
                    setGroupedCards(res.data);
                    scrollToCards();
                } catch (error) {
                    console.error('Ошибка при загрузке всех карт:', error);
                    setGroupedCards([]);
                } finally {
                    setIsLoading(false);
                }

                return;
            }
            setIsLoading(true);
            try {
                const res = await axios.get(`${API}/main_categories/${activeMainCategory}/details`);
                const { subcategories, cards } = res.data;

                setSubCategories(subcategories);
                setGroupedCards(groupCardsByBank(cards));
                scrollToCards();
            } catch (error) {
                console.error('Ошибка при загрузке деталей категории:', error);
                setSubCategories([]);
                setGroupedCards([]);
            } finally {
                setIsLoading(false);
            }
        };
        fetchData();
    }, [activeMainCategory]);

    useEffect(() => {
        const fetchData = async () => {
            if (!activeSubCategory) {
                if (activeMainCategory) {
                    setIsLoading(true);
                    try {
                        const res = await axios.get(`${API}/main_categories/${activeMainCategory}/details`);
                        const { cards } = res.data;

                        setGroupedCards(groupCardsByBank(cards));
                        scrollToCards();
                    } catch (error) {
                        console.error('Ошибка при загрузке карт категории:', error);
                        setGroupedCards([]);
                    } finally {
                        setIsLoading(false);
                    }
                }

                return;
            }
            setIsLoading(true);
            try {
                const res = await axios.get(`${API}/cards/by_subcategory/${activeSubCategory}/cards`);
                setGroupedCards(groupCardsByBank(res.data));
                scrollToCards();
            } catch (error) {
                console.error('Ошибка при загрузке карт подкатегории:', error);
            } finally {
                setIsLoading(false);
            }
        };
        fetchData();
    }, [activeSubCategory]);

    const scrollToCards = () => {
        // if (cardsSectionRef.current) {
        //     cardsSectionRef.current.scrollIntoView({ behavior: 'smooth' });
        // }
    };
    const [activeImageKey, setActiveImageKey] = useState(null);
    return (
        <div className="flex flex-col items-center w-full min-h-screen">
            <HeaderLinks />
            <Header />
            {/* <MainCategories
                categories={mainCategories}
                activeCategory={activeMainCategory}
                onSelectCategory={(id) => setActiveMainCategory(id === activeMainCategory ? null : id)}
            /> */}

            <CategoryImageSelector
                value={activeImageKey}
                onSelect={(key) => {
                    setActiveImageKey(key);

                    if (!key) {
                        setActiveMainCategory(null);
                        return;
                    }
                    const selected = mainCategories.find(cat => cat.name === key.toUpperCase());
                    setActiveMainCategory(selected?.id || null);
                }}
            />
            <SubCategories
                subCategories={subCategories}
                activeSubCategory={activeSubCategory}
                onSelectSubCategory={(id) => setActiveSubCategory(id === activeSubCategory ? null : id)}
            />
            <div ref={cardsSectionRef} className="w-full flex justify-center min-h-[20rem] relative">
                <CardList groupedCards={groupedCards} />
                {groupedCards.length === 0 && (
                    <div className="absolute">
                        <img src={noCardsImg} alt="No cards" className="h-auto" />
                    </div>
                )}
            </div>
        </div>
    );
}
