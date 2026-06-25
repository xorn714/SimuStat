import React from 'react'

export type TabType = 'dashboard' | 'modelos' | 'analiticas'

interface NavbarProps {
    activeTab: TabType
    setActiveTab: (tab: TabType) => void
}

export const Navbar: React.FC<NavbarProps> = ({ activeTab, setActiveTab }) => {
    const navItems: { id: TabType; label: string }[] = [
        { id: 'dashboard', label: 'Dashboard' },
        { id: 'modelos', label: 'Modelos' },
        { id: 'analiticas', label: 'Analíticas' },
    ]

    return (
        <nav className="border-b border-slate-800 bg-[#171F33] backdrop-blur-xl sticky top-0 z-50">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
                <div className="flex items-center gap-8">
                    {/* Logo */}
                    <div className="flex items-center gap-2 cursor-pointer" onClick={() => setActiveTab('dashboard')}>
                        <span className="text-2xl  tracking-wider text-primary font-headline">
                            SimuStat
                        </span>
                    </div>

                    {/* Enlaces de navegación */}
                    <div className="flex items-center gap-6">
                        {navItems.map((item) => (
                            <button
                                key={item.id}
                                onClick={() => setActiveTab(item.id)}
                                className={`text-sm font-semibold transition-colors duration-200 cursor-pointer ${activeTab === item.id
                                        ? 'text-primary'
                                        : 'text-white hover:text-primary/80'
                                    }`}
                            >
                                {item.label}
                            </button>
                        ))}
                    </div>
                </div>
            </div>
        </nav>
    )
}
