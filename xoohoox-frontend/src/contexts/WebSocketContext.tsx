import React, { createContext, useContext, useEffect, useState } from 'react';
import { websocketService } from '../services/websocketService';

interface WebSocketContextType {
  isConnected: boolean;
  connect: (url: string) => void;
  disconnect: () => void;
}

const WebSocketContext = createContext<WebSocketContextType | undefined>(undefined);

export const WebSocketProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [isConnected, setIsConnected] = useState(false);

  useEffect(() => {
    const handleConnect = () => setIsConnected(true);
    const handleDisconnect = () => setIsConnected(false);

    websocketService.on('connect', handleConnect);
    websocketService.on('disconnect', handleDisconnect);

    // Initial connection
    websocketService.connect(process.env.REACT_APP_WS_URL || 'ws://localhost:8000/ws');

    return () => {
      websocketService.off('connect', handleConnect);
      websocketService.off('disconnect', handleDisconnect);
      websocketService.disconnect();
    };
  }, []);

  const value = {
    isConnected,
    connect: (url: string) => websocketService.connect(url),
    disconnect: () => websocketService.disconnect(),
  };

  return (
    <WebSocketContext.Provider value={value}>
      {children}
    </WebSocketContext.Provider>
  );
};

export const useWebSocketContext = () => {
  const context = useContext(WebSocketContext);
  if (context === undefined) {
    throw new Error('useWebSocketContext must be used within a WebSocketProvider');
  }
  return context;
}; 