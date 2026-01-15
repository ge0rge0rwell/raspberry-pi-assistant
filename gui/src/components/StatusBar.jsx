import React, { useState, useEffect } from 'react';
import { Cpu, Thermometer, Wifi, Battery, Clock } from 'lucide-react';

const StatusBar = () => {
    const [stats, setStats] = useState({
        cpu_usage: 0,
        memory_usage: 0,
        temperature: 0,
        uptime: "0:00"
    });
    const [time, setTime] = useState(new Date());

    useEffect(() => {
        const timer = setInterval(() => setTime(new Date()), 1000);
        const statsTimer = setInterval(async () => {
            try {
                const res = await fetch('http://localhost:8000/stats');
                const data = await res.json();
                setStats(data);
            } catch (e) {
                console.error("Failed to fetch stats", e);
            }
        }, 5000);

        return () => {
            clearInterval(timer);
            clearInterval(statsTimer);
        };
    }, []);

    return (
        <div className="fixed top-0 left-0 right-0 h-10 px-6 flex items-center justify-between liquid-glass border-t-0 border-x-0 rounded-none z-50">
            <div className="flex items-center gap-6 text-xs font-medium text-white/70">
                <div className="flex items-center gap-2">
                    <Cpu size={14} className="text-brand-primary" />
                    <span>{stats.cpu_usage}%</span>
                </div>
                <div className="flex items-center gap-2">
                    <Thermometer size={14} className="text-brand-secondary" />
                    <span>{stats.temperature}°C</span>
                </div>
            </div>

            <div className="absolute left-1/2 -translate-x-1/2 flex items-center gap-2">
                <div className="w-2 h-2 rounded-full bg-green-500 pulse-glow" />
                <span className="text-xs font-bold tracking-widest uppercase">Nova OS</span>
            </div>

            <div className="flex items-center gap-6 text-xs font-medium text-white/70">
                <div className="flex items-center gap-2">
                    <Wifi size={14} />
                    <span>Online</span>
                </div>
                <div className="flex items-center gap-2">
                    <Clock size={14} />
                    <span>{time.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}</span>
                </div>
            </div>
        </div>
    );
};

export default StatusBar;
