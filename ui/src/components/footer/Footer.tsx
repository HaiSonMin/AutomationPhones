import { useState, useEffect } from 'react';
import { Typography, Space } from 'antd';
import { PhoneOutlined, CheckCircleOutlined, CloseCircleOutlined } from '@ant-design/icons';
import { useThemeStore } from '../../stores/themeStore';

const { Text } = Typography;

interface FooterProps {
  version?: string;
}

interface StatusInfo {
  serverConnected: boolean;
  devicesRunning: number;
  devicesStopped: number;
  toolRunning: boolean;
}

/**
 * Chức các thông tin như:
 * - Version
 * - Số Device đang chạy
 * - Số Device dừng
 * - Trạng thái connect với server
 * - Trạng thái tool (start/stop)
 *
 */

const Footer: React.FC<FooterProps> = ({ version = '1.0.0' }) => {
  const { mode: themeMode } = useThemeStore();
  const isDark = themeMode === 'dark';

  const [status, setStatus] = useState<StatusInfo>({
    serverConnected: false,
    devicesRunning: 0,
    devicesStopped: 0,
    toolRunning: false,
  });

  useEffect(() => {
    // Load initial status
    loadStatus();

    // Update status every 5 seconds
    const interval = setInterval(loadStatus, 5000);

    return () => clearInterval(interval);
  }, []);

  const loadStatus = async () => {
    try {
      // Check if PyWebView API is available
      if (!window.pywebview?.api) {
        console.error('PyWebView API not available');
        return;
      }

      // Get health status from Python
      const health = await window.pywebview.api.health_check_health_server();

      setStatus({
        serverConnected: health.server,
        devicesRunning: health.devices || 0,
        devicesStopped: 0, // TODO: Get stopped devices count
        toolRunning: false, // TODO: Get tool running status
      });
    } catch (error) {
      console.error('Failed to load status:', error);
      setStatus({
        ...status,
        serverConnected: false,
      });
    }
  };

  return (
    <div
      style={{
        textAlign: 'right',
        padding: '12px 24px',
        borderTop: isDark ? '1px solid #303030' : '1px solid #f0f0f0',
        background: isDark ? '#1f1f1f' : '#fff',
      }}
    >
      <Space split={<span style={{ color: isDark ? '#434343' : '#d9d9d9' }}>|</span>}>
        {/* Server Connection Status */}
        <Space size={4}>
          {status.serverConnected ? (
            <CheckCircleOutlined style={{ color: '#52c41a', fontSize: '12px' }} />
          ) : (
            <CloseCircleOutlined style={{ color: '#ff4d4f', fontSize: '12px' }} />
          )}
          <Text style={{ color: status.serverConnected ? '#52c41a' : '#ff4d4f', fontSize: '12px' }}>
            Server {status.serverConnected ? 'Connected' : 'Disconnected'}
          </Text>
        </Space>

        {/* Device Status */}
        <Space size={4}>
          <PhoneOutlined style={{ fontSize: '12px', color: isDark ? '#8c8c8c' : undefined }} />
          <Text style={{ fontSize: '12px', color: isDark ? '#8c8c8c' : '#8c8c8c' }}>
            Devices:{' '}
            <Text style={{ color: '#52c41a', fontSize: '12px' }}>
              {status.devicesRunning} running
            </Text>
            <Text style={{ color: isDark ? '#595959' : '#8c8c8c', fontSize: '12px' }}>
              / {status.devicesStopped} stopped
            </Text>
          </Text>
        </Space>

        {/* Version */}
        <Text style={{ fontSize: '12px', color: isDark ? '#8c8c8c' : '#8c8c8c' }}>
          Version {version}
        </Text>
      </Space>
    </div>
  );
};

export default Footer;
