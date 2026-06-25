import React from 'react'

export const Navbar: React.FC = () => {
    return (
        <nav className="border-b border-slate-800 bg-[#171F33] backdrop-blur-xl sticky top-0 z-50">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
                <div className="flex items-center gap-8">
                    {/* Logo / Marca */}
                    <div className="flex items-center gap-2">
                        <span className="text-2xl tracking-wider text-primary font-headline">
                            SimuStat
                        </span>
                    </div>
                </div>

                {/* Indicador de estado */}
                <div className="flex items-center gap-2">
                    <span className="flex h-2 w-2 relative">
                        <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-secondary opacity-75"></span>
                        <span className="relative inline-flex rounded-full h-2 w-2 bg-secondary"></span>
                    </span>
                    <span className="text-xs text-slate-400 font-label hidden sm:inline">Backend Online</span>
                </div>
            </div>
        </nav>
    )
}
