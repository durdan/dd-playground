class WebSocketClient {
    constructor(url = 'ws://localhost:8765') {
        this.url = url;
        this.ws = null;
        this.reconnectAttempts = 0;
        this.maxReconnectAttempts = 5;
        this.reconnectDelay = 1000;
        this.messageHandlers = new Map();
        this.connectionState = 'disconnected';
    }
    
    connect() {
        try {
            this.ws = new WebSocket(this.url);
            this.setupEventHandlers();
        } catch (error) {
            console.error('WebSocket connection failed:', error);
            this.handleReconnect();
        }
    }
    
    setupEventHandlers() {
        this.ws.onopen = () => {
            console.log('WebSocket connected');
            this.connectionState = 'connected';
            this.reconnectAttempts = 0;
            this.notifyConnectionChange('connected');
        };
        
        this.ws.onmessage = (event) => {
            try {
                const message = JSON.parse(event.data);
                this.handleMessage(message);
            } catch (error) {
                console.error('Failed to parse message:', error);
            }
        };
        
        this.ws.onclose = () => {
            console.log('WebSocket disconnected');
            this.connectionState = 'disconnected';
            this.notifyConnectionChange('disconnected');
            this.handleReconnect();
        };
        
        this.ws.onerror = (error) => {
            console.error('WebSocket error:', error);
            this.connectionState = 'error';
            this.notifyConnectionChange('error');
        };
    }
    
    handleMessage(message) {
        const handler = this.messageHandlers.get(message.type);
        if (handler) {
            handler(message);
        } else {
            console.warn('No handler for message type:', message.type);
        }
    }
    
    onMessage(type, handler) {
        this.messageHandlers.set(type, handler);
    }
    
    onConnectionChange(handler) {
        this.connectionChangeHandler = handler;
    }
    
    notifyConnectionChange(state) {
        if (this.connectionChangeHandler) {
            this.connectionChangeHandler(state);
        }
    }
    
    send(message) {
        if (this.ws && this.ws.readyState === WebSocket.OPEN) {
            this.ws.send(JSON.stringify(message));
            return true;
        } else {
            console.error('WebSocket not connected');
            return false;
        }
    }
    
    handleReconnect() {
        if (this.reconnectAttempts < this.maxReconnectAttempts) {
            this.reconnectAttempts++;
            console.log(`Attempting to reconnect... (${this.reconnectAttempts}/${this.maxReconnectAttempts})`);
            
            setTimeout(() => {
                this.connect();
            }, this.reconnectDelay * this.reconnectAttempts);
        } else {
            console.error('Max reconnection attempts reached');
            this.connectionState = 'failed';
            this.notifyConnectionChange('failed');
        }
    }
    
    disconnect() {
        if (this.ws) {
            this.ws.close();
            this.ws = null;
        }
    }
    
    getConnectionState() {
        return this.connectionState;
    }
}