import React, { useState, useEffect, useRef } from 'react';
import { Mic, MessageSquare, Volume2, Settings, Command } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

const Dashboard = () => {
    const [messages, setMessages] = useState([
        { role: 'assistant', text: 'Ready for your command.' }
    ]);
    const [state, setState] = useState('idle'); // idle, listening, processing, speaking
    const [amplitude, setAmplitude] = useState(0);
    const messagesEndRef = useRef(null);
    const socketRef = useRef(null);

    useEffect(() => {
        socketRef.current = new WebSocket('ws://localhost:8000/ws');

        socketRef.current.onmessage = (event) => {
            const { type, data } = JSON.parse(event.data);
            if (type === 'state') {
                setState(data.status);
                if (data.amplitude) setAmplitude(data.amplitude);
            } else if (type === 'transcript') {
                setMessages(prev => [...prev.slice(-10), data]);
            }
        };

        return () => socketRef.current?.close();
    }, []);

    useEffect(() => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, [messages]);

    return (
        <div className="relative flex flex-col items-center justify-center h-screen w-screen pt-10">
            <div className="aurora-bg" />

            {/* Central Visualizer */}
            <div className="relative z-10 flex flex-col items-center gap-12">
                <div className="relative">
                    {/* Outer Ring */}
                    <motion.div
                        animate={{
                            rotate: 360,
                            scale: state === 'listening' ? [1, 1.1, 1] : 1
                        }}
                        transition={{
                            rotate: { duration: 20, repeat: Infinity, ease: "linear" },
                            scale: { duration: 2, repeat: Infinity }
                        }}
                        className="w-64 h-64 rounded-full border-2 border-brand-primary/20 flex items-center justify-center"
                    >
                        <div className="w-60 h-60 rounded-full border border-brand-secondary/30 flex items-center justify-center p-4">
                            <div className="w-full h-full rounded-full liquid-glass flex items-center justify-center overflow-hidden">
                                {/* AI Core Waveform */}
                                <div className="flex items-end gap-1 px-4 h-12">
                                    {[...Array(12)].map((_, i) => (
                                        <motion.div
                                            key={i}
                                            animate={{
                                                height: state === 'listening' ? Math.random() * 40 + 10 : 8
                                            }}
                                            className="w-1.5 bg-gradient-to-t from-brand-primary to-brand-accent rounded-full"
                                        />
                                    ))}
                                </div>
                            </div>
                        </div>
                    </motion.div>

                    {/* Status Label */}
                    <div className="absolute -bottom-16 left-1/2 -translate-x-1/2 text-center">
                        <h2 className="text-2xl font-display font-light tracking-widest text-shimmer uppercase">
                            {state.replace('_', ' ')}
                        </h2>
                        <p className="text-[10px] text-white/40 mt-1 uppercase tracking-tighter">AI Core Active</p>
                    </div>
                </div>
            </div>

            {/* Chat History Overlay */}
            <div className="absolute right-8 top-24 bottom-24 w-80 flex flex-col gap-4">
                <div className="flex-1 overflow-y-auto pr-4 scrollbar-hide flex flex-col gap-4">
                    <AnimatePresence>
                        {messages.map((msg, i) => (
                            <motion.div
                                key={i}
                                initial={{ opacity: 0, x: 20 }}
                                animate={{ opacity: 1, x: 0 }}
                                className={`p-4 rounded-2xl liquid-glass text-sm ${msg.role === 'user' ? 'border-brand-primary/40 bg-brand-primary/5' : ''
                                    }`}
                            >
                                <div className="text-[10px] uppercase tracking-widest text-white/40 mb-1">
                                    {msg.role}
                                </div>
                                {msg.text}
                            </motion.div>
                        ))}
                    </AnimatePresence>
                    <div ref={messagesEndRef} />
                </div>
            </div>

            {/* Quick Launch Bar */}
            <div className="absolute bottom-8 left-1/2 -translate-x-1/2 flex items-center gap-4 px-6 py-3 rounded-2xl liquid-glass">
                <button className="p-2 hover:bg-white/10 rounded-xl transition-colors">
                    <Command size={20} className="text-white/60" />
                </button>
                <div className="w-px h-6 bg-white/10" />
                <button className="p-2 hover:bg-white/10 rounded-xl transition-colors">
                    <Mic size={20} className={state === 'listening' ? 'text-red-400 pulse-glow' : 'text-white/60'} />
                </button>
                <button className="p-2 hover:bg-white/10 rounded-xl transition-colors">
                    <MessageSquare size={20} className="text-white/60" />
                </button>
                <button className="p-2 hover:bg-white/10 rounded-xl transition-colors">
                    <Settings size={20} className="text-white/60" />
                </button>
            </div>
        </div>
    );
};

export default Dashboard;
