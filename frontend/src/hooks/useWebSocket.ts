import {useEffect, useRef, useCallback} from 'react';

interface UseWebSocketProps {
  url: string;
  onMessage: (data: any) => void;
  onOpen?: () => void;
  onClose?: () => void;
  onError?: (error: Event) => void;
}

export const useWebSocket = ({url, onMessage, onOpen, onClose, onError}: UseWebSocketProps) => {
    const websocketRef = useRef<WebSocket | null>(null);

    useEffect(() => {
        const ws = new WebSocket(url);
        websocketRef.current = ws;

        ws.onopen = () => onOpen?.();
        
        ws.onmessage = (event) => {
            const data = JSON.parse(event.data)
            onMessage(data)
        }

        ws.onerror = (error) => onError?.(error);
        
        ws.onclose = () => onClose?.();

        return () => {
            if (ws.readyState === WebSocket.OPEN) {
                ws.close()
            }
        };
    }, [url, onMessage, onOpen, onClose, onError])

    const sendMessage = useCallback((data: any) => {
    if (websocketRef.current?.readyState === WebSocket.OPEN) {
      websocketRef.current.send(JSON.stringify(data));
    }
  }, [])
  return {sendMessage}
}