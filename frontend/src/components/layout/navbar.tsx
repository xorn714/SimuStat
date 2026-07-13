import React, { useState, useEffect } from 'react'
import { checkBackendStatus } from '../../services/api'

export const Navbar: React.FC = () => {
    const [status, setStatus] = useState<'online' | 'offline' | 'checking'>('checking')

    useEffect(() => {
        const verifyStatus = async () => {
            const isOnline = await checkBackendStatus()
            setStatus(isOnline ? 'online' : 'offline')
        }

        verifyStatus()
        const interval = setInterval(verifyStatus, 10000) // Verificar cada 10 segundos

        return () => clearInterval(interval)
    }, [])

    return (
        <nav className="border-b border-slate-800 bg-[#171F33] backdrop-blur-xl sticky top-0 z-50">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
                {/* Logo / Marca */}
                <div className="flex items-center gap-2">
                    <span className="text-2xl tracking-wider text-primary font-headline">
                        SimuStat
                    </span>
                </div>

                {/* Indicador de estado */}
                <div className="flex items-center gap-2">
                    <span className="flex h-2 w-2 relative">
                        {status === 'checking' && (
                            <>
                                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-yellow-500 opacity-75"></span>
                                <span className="relative inline-flex rounded-full h-2 w-2 bg-yellow-500"></span>
                            </>
                        )}
                        {status === 'online' && (
                            <>
                                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-[#4EDEA3] opacity-75"></span>
                                <span className="relative inline-flex rounded-full h-2 w-2 bg-[#4EDEA3]"></span>
                            </>
                        )}
                        {status === 'offline' && (
                            <>
                                <span className="relative inline-flex rounded-full h-2 w-2 bg-red-500"></span>
                            </>
                        )}
                    </span>
                    <span className="text-xs text-slate-400 font-label hidden sm:inline">
                        {status === 'checking' && 'Conectando...'}
                        {status === 'online' && 'Backend Online'}
                        {status === 'offline' && 'Backend Offline'}
                    </span>
                </div>
            </div>
        </nav>
    )
}

