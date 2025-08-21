import { useEffect, useRef, useState, useCallback } from 'react';
import { io, Socket } from 'socket.io-client';

interface UseSocketOptions {
  url?: string;
  autoConnect?: boolean;
  reconnectionAttempts?: number;
  reconnectionDelay?: number;
}

interface UseSocketReturn {
  socket: Socket | null;
  isConnected: boolean;
  connect: () => void;
  disconnect: () => void;
  emit: (event: string, data: any) => void;
  on: (event: string, callback: (data: any) => void) => void;
  off: (event: string, callback?: (data: any) => void) => void;
}

export const useSocket = ({
  url = 'http://localhost:3000',
  autoConnect = true,
  reconnectionAttempts = 5,
  reconnectionDelay = 1000
}: UseSocketOptions = {}): UseSocketReturn => {
  const [isConnected, setIsConnected] = useState(false);
  const socketRef = useRef<Socket | null>(null);
  const reconnectAttemptsRef = useRef(0);

  const connect = useCallback(() => {
    if (socketRef.current?.connected) return;

    const socket = io(url, {
      reconnection: true,
      reconnectionAttempts,
      reconnectionDelay,
    });

    socket.on('connect', () => {
      console.log('Socket connected');
      setIsConnected(true);
      reconnectAttemptsRef.current = 0;
    });

    socket.on('disconnect', () => {
      console.log('Socket disconnected');
      setIsConnected(false);
    });

    socket.on('connect_error', (error) => {
      console.error('Socket connection error:', error);
      reconnectAttemptsRef.current += 1;
      
      if (reconnectAttemptsRef.current >= reconnectionAttempts) {
        console.error('Max reconnection attempts reached');
        socket.disconnect();
      }
    });

    socketRef.current = socket;
  }, [url, reconnectionAttempts, reconnectionDelay]);

  const disconnect = useCallback(() => {
    if (socketRef.current) {
      socketRef.current.disconnect();
      socketRef.current = null;
      setIsConnected(false);
    }
  }, []);

  const emit = useCallback((event: string, data: any) => {
    if (socketRef.current) {
      socketRef.current.emit(event, data);
    } else {
      console.warn('Socket not connected. Cannot emit event:', event);
    }
  }, []);

  const on = useCallback((event: string, callback: (data: any) => void) => {
    if (socketRef.current) {
      socketRef.current.on(event, callback);
    } else {
      console.warn('Socket not connected. Cannot add listener for event:', event);
    }
  }, []);

  const off = useCallback((event: string, callback?: (data: any) => void) => {
    if (socketRef.current) {
      if (callback) {
        socketRef.current.off(event, callback);
      } else {
        socketRef.current.off(event);
      }
    }
  }, []);

  useEffect(() => {
    if (autoConnect) {
      connect();
    }

    return () => {
      disconnect();
    };
  }, [autoConnect, connect, disconnect]);

  return {
    socket: socketRef.current,
    isConnected,
    connect,
    disconnect,
    emit,
    on,
    off
  };
};

export default useSocket; 