import React, { useEffect, useRef, useState } from 'react';
import { Card, Spin, Alert, Button } from 'antd';
import { PlayCircleOutlined, StopOutlined } from '@ant-design/icons';

interface VideoDisplayProps {
  deviceId: string;
  deviceName: string;
  isActive: boolean;
  onConnect: () => void;
  onDisconnect: () => void;
}

const VideoDisplay: React.FC<VideoDisplayProps> = ({
  deviceId,
  deviceName,
  isActive,
  onConnect,
  onDisconnect,
}) => {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const [isConnected, setIsConnected] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [ws, setWs] = useState<WebSocket | null>(null);

  useEffect(() => {
    if (isActive && !ws) {
      connectWebSocket();
    } else if (!isActive && ws) {
      disconnectWebSocket();
    }

    return () => {
      if (ws) {
        ws.close();
      }
    };
  }, [isActive]);

  const connectWebSocket = () => {
    try {
      const websocket = new WebSocket('ws://localhost:8765');

      websocket.onopen = () => {
        console.log(`WebSocket connected for device ${deviceId}`);
        setIsConnected(true);
        setError(null);

        // Subscribe to device stream
        websocket.send(
          JSON.stringify({
            type: 'subscribe',
            device_id: deviceId,
          })
        );
      };

      websocket.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);

          if (data.type === 'video_frame' && data.device_id === deviceId) {
            // For now, just log that we received a frame
            // In a real implementation, you'd decode the H.264 frame
            // and render it to the canvas
            console.log(`Received frame for ${deviceId}, size: ${data.data?.length || 0}`);

            // Placeholder: Draw a placeholder image
            const canvas = canvasRef.current;
            if (canvas) {
              const ctx = canvas.getContext('2d');
              if (ctx) {
                ctx.fillStyle = '#1a1a1a';
                ctx.fillRect(0, 0, canvas.width, canvas.height);
                ctx.fillStyle = '#fff';
                ctx.font = '16px Arial';
                ctx.textAlign = 'center';
                ctx.fillText(`Device: ${deviceName}`, canvas.width / 2, canvas.height / 2 - 20);
                ctx.fillText(`ID: ${deviceId}`, canvas.width / 2, canvas.height / 2);
                ctx.fillText('Streaming...', canvas.width / 2, canvas.height / 2 + 20);
              }
            }
          } else if (data.type === 'stream_ended') {
            console.log(`Stream ended for ${deviceId}`);
            setIsConnected(false);
          }
        } catch (err) {
          console.error('Error parsing WebSocket message:', err);
        }
      };

      websocket.onclose = () => {
        console.log(`WebSocket disconnected for device ${deviceId}`);
        setIsConnected(false);
        setWs(null);
      };

      websocket.onerror = (error) => {
        console.error(`WebSocket error for device ${deviceId}:`, error);
        setError('Failed to connect to video stream');
        setIsConnected(false);
      };

      setWs(websocket);
    } catch (err) {
      console.error('Error creating WebSocket:', err);
      setError('Failed to initialize video stream');
    }
  };

  const disconnectWebSocket = () => {
    if (ws) {
      ws.close();
      setWs(null);
    }
    setIsConnected(false);
  };

  const handleConnect = () => {
    onConnect();
  };

  const handleDisconnect = () => {
    disconnectWebSocket();
    onDisconnect();
  };

  return (
    <Card
      title={
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <span>{deviceName}</span>
          <span style={{ fontSize: '12px', color: '#666' }}>{deviceId}</span>
        </div>
      }
      extra={
        <Button
          type={isActive ? 'default' : 'primary'}
          icon={isActive ? <StopOutlined /> : <PlayCircleOutlined />}
          onClick={isActive ? handleDisconnect : handleConnect}
          danger={isActive}
        >
          {isActive ? 'Disconnect' : 'Connect'}
        </Button>
      }
      style={{ width: '100%', maxWidth: 800 }}
    >
      {error && (
        <Alert
          message='Error'
          description={error}
          type='error'
          showIcon
          style={{ marginBottom: 16 }}
        />
      )}

      <div style={{ position: 'relative', backgroundColor: '#000', borderRadius: 8 }}>
        <canvas
          ref={canvasRef}
          width={800}
          height={600}
          style={{
            width: '100%',
            height: 'auto',
            display: 'block',
            borderRadius: 8,
          }}
        />

        {!isActive && !isConnected && (
          <div
            style={{
              position: 'absolute',
              top: 0,
              left: 0,
              right: 0,
              bottom: 0,
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              backgroundColor: 'rgba(0, 0, 0, 0.7)',
              borderRadius: 8,
            }}
          >
            <div style={{ textAlign: 'center', color: '#fff' }}>
              <PlayCircleOutlined style={{ fontSize: 48, marginBottom: 16 }} />
              <div>Click Connect to start streaming</div>
            </div>
          </div>
        )}

        {isActive && !isConnected && (
          <div
            style={{
              position: 'absolute',
              top: 0,
              left: 0,
              right: 0,
              bottom: 0,
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              backgroundColor: 'rgba(0, 0, 0, 0.7)',
              borderRadius: 8,
            }}
          >
            <Spin size='large' />
          </div>
        )}

        {isConnected && (
          <div
            style={{
              position: 'absolute',
              top: 8,
              right: 8,
              backgroundColor: 'rgba(0, 255, 0, 0.2)',
              color: '#0f0',
              padding: '4px 8px',
              borderRadius: 4,
              fontSize: '12px',
            }}
          >
            ● LIVE
          </div>
        )}
      </div>
    </Card>
  );
};

export default VideoDisplay;
