'use client';

import { useState } from 'react';

export default function RecipeFinder() {
    const [search, setSearch] = useState('');

    return (
        <div className="max-w-6xl mx-auto p-8">
            <h1 className="text-4xl font-bold mb-8 text-center">
                Recipe Finder
            </h1>

            <div className="mb-8">
                <input
                    type="text"
                    placeholder="Suche nach Rezepten..."
                    value={search}
                    onChange={(e) => setSearch(e.target.value)}
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
            </div>
        </div>
    );

}