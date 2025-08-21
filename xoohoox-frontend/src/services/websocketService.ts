import { io, Socket } from 'socket.io-client';

type EventCallback = (data: any) => void;

class WebSocketService {
  private socket: Socket | null = null;
  private isConnected: boolean = false;
  private reconnectAttempts: number = 0;
  private readonly maxReconnectAttempts: number = 5;
  private readonly reconnectDelay: number = 1000;
  private eventListeners: Map<string, Set<EventCallback>> = new Map();

  constructor() {
    this.setupEventHandlers();
  }

  private setupEventHandlers(): void {
    this.on('connect', () => {
      this.isConnected = true;
      this.reconnectAttempts = 0;
    });

    this.on('disconnect', () => {
      this.isConnected = false;
    });
  }

  public connect(url: string): void {
    if (this.socket) {
      this.socket.disconnect();
    }

    this.socket = io(url, {
      reconnection: true,
      reconnectionAttempts: this.maxReconnectAttempts,
      reconnectionDelay: this.reconnectDelay,
    });

    this.setupSocketListeners();
  }

  private setupSocketListeners(): void {
    if (!this.socket) return;

    this.socket.on('connect', () => {
      this.emit('connected');
    });

    this.socket.on('disconnect', () => {
      this.emit('disconnected');
    });

    this.socket.on('error', (error: Error) => {
      this.emit('error', error);
    });

    this.socket.on('reconnect_attempt', (attemptNumber: number) => {
      this.emit('reconnect_attempt', attemptNumber);
    });

    this.socket.on('reconnect_failed', () => {
      this.emit('reconnect_failed');
    });
  }

  public on(event: string, callback: EventCallback): void {
    if (!this.eventListeners.has(event)) {
      this.eventListeners.set(event, new Set());
    }
    this.eventListeners.get(event)?.add(callback);
  }

  public off(event: string, callback: EventCallback): void {
    this.eventListeners.get(event)?.delete(callback);
  }

  public emit(event: string, data?: any): void {
    if (!this.socket || !this.isConnected) {
      throw new Error('Socket is not connected');
    }

    this.socket.emit(event, data);
    this.eventListeners.get(event)?.forEach(callback => callback(data));
  }

  public subscribe(event: string, callback: EventCallback): void {
    if (!this.socket || !this.isConnected) {
      throw new Error('Socket is not connected');
    }

    this.socket.on(event, callback);
  }

  public unsubscribe(event: string, callback: EventCallback): void {
    if (!this.socket) return;

    this.socket.off(event, callback);
  }

  public disconnect(): void {
    if (this.socket) {
      this.socket.disconnect();
      this.socket = null;
      this.isConnected = false;
    }
  }
}

export const websocketService = new WebSocketService(); 