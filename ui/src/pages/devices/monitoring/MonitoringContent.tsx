/**
 * MonitoringContent - Content component for device monitoring
 *
 * This contains the actual monitoring UI (grid, devices, etc).
 * Separated from MonitoringPage so it can be wrapped in DashboardLayout.
 *
 * Features:
 * - Auto-fetch devices on mount
 * - Real-time updates via Python events
 * - Polling fallback every 5 seconds
 * - Disconnect all button
 * - Responsive grid layout
 */

import React, { useState, useEffect, useCallback } from 'react';
import { Typography, Spin, Alert, Button, Space, Card, Row, Col, Statistic, Badge } from 'antd';
import {
  ReloadOutlined,
  DisconnectOutlined,
  MobileOutlined,
  PlayCircleOutlined,
} from '@ant-design/icons';
import { useMonitoringBridge } from './hooks/useMonitoringBridge';
import { useDeviceEvents } from './hooks/useDeviceEvents';
import { DeviceGrid } from './components/DeviceGrid';
import type { Device } from './types/monitoring.types';

const { Title, Text } = Typography;

// =============================================================================
// CONSTANTS
// =============================================================================

/** How often to poll for devices (in milliseconds) */
const POLL_INTERVAL_MS = 5000;

// =============================================================================
// COMPONENT
// =============================================================================

const MonitoringContent: React.FC = () => {
  const bridge = useMonitoringBridge();

  // State
  const [devices, setDevices] = useState<Device[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // =========================================================================
  // FETCH DEVICES
  // =========================================================================

  /**
   * Fetch device list from Python bridge
   */
  const fetchDevices = useCallback(async () => {
    try {
      const data = await bridge.getDevices();
      setDevices(data);
      setError(null);
    } catch (err) {
      console.error('[MonitoringContent] Failed to fetch devices:', err);
      setError('Không thể tải danh sách thiết bị');
    } finally {
      setLoading(false);
    }
  }, [bridge]);

  /**
   * Refresh devices (with loading state)
   */
  const handleRefresh = useCallback(async () => {
    setLoading(true);
    await fetchDevices();
  }, [fetchDevices]);

  // =========================================================================
  // DISCONNECT ALL
  // =========================================================================

  /**
   * Disconnect all streaming devices
   */
  const handleDisconnectAll = useCallback(async () => {
    try {
      await bridge.disconnectAll();
      await fetchDevices();
    } catch (err) {
      console.error('[MonitoringContent] Failed to disconnect all:', err);
    }
  }, [bridge, fetchDevices]);

  // =========================================================================
  // EVENT HANDLING
  // =========================================================================

  /**
   * Handle device changes from Python events
   */
  const handleDevicesChanged = useCallback((updatedDevices: Device[]) => {
    console.log('[MonitoringContent] Devices changed:', updatedDevices.length);
    setDevices(updatedDevices);
  }, []);

  // Subscribe to events from Python
  useDeviceEvents(handleDevicesChanged);

  // =========================================================================
  // EFFECTS
  // =========================================================================

  // Initial fetch on mount
  useEffect(() => {
    fetchDevices();
  }, [fetchDevices]);

  // Polling fallback (in case events don't work)
  useEffect(() => {
    const interval = setInterval(() => {
      // Only poll if not currently loading
      if (!loading) {
        fetchDevices();
      }
    }, POLL_INTERVAL_MS);

    return () => clearInterval(interval);
  }, [fetchDevices, loading]);

  // =========================================================================
  // COMPUTED VALUES
  // =========================================================================

  const onlineCount = devices.filter((d) => d.is_online).length;
  const streamingCount = devices.filter((d) => d.is_streaming).length;

  // =========================================================================
  // RENDER
  // =========================================================================

  return (
    <div>
      {/* Page Header */}
      <div style={{ marginBottom: 24 }}>
        <Title level={4} style={{ margin: 0, marginBottom: 8 }}>
          📱 Device Monitoring
        </Title>
        <Text type='secondary'>Quản lý và theo dõi thiết bị Android kết nối qua USB</Text>
      </div>

      {/* Stats Row */}
      <Row gutter={16} style={{ marginBottom: 24 }}>
        <Col span={6}>
          <Card size='small'>
            <Statistic title='Tổng thiết bị' value={devices.length} prefix={<MobileOutlined />} />
          </Card>
        </Col>
        <Col span={6}>
          <Card size='small'>
            <Statistic title='Online' value={onlineCount} valueStyle={{ color: '#52c41a' }} />
          </Card>
        </Col>
        <Col span={6}>
          <Card size='small'>
            <Badge dot={streamingCount > 0} offset={[10, 0]}>
              <Statistic
                title='Đang stream'
                value={streamingCount}
                prefix={<PlayCircleOutlined />}
                valueStyle={{ color: '#1890ff' }}
              />
            </Badge>
          </Card>
        </Col>
        <Col span={6}>
          <Card size='small'>
            <Space>
              <Button
                icon={<ReloadOutlined spin={loading} />}
                onClick={handleRefresh}
                loading={loading}
              >
                Refresh
              </Button>
              {streamingCount > 0 && (
                <Button icon={<DisconnectOutlined />} onClick={handleDisconnectAll} danger>
                  Ngắt tất cả
                </Button>
              )}
            </Space>
          </Card>
        </Col>
      </Row>

      {/* Error Banner */}
      {error && (
        <Alert
          message='Lỗi'
          description={error}
          type='error'
          showIcon
          closable
          style={{ marginBottom: 24 }}
          action={
            <Button size='small' onClick={handleRefresh}>
              Thử lại
            </Button>
          }
        />
      )}

      {/* Bridge Status */}
      {!bridge.isAvailable && (
        <Alert
          message='Chế độ Demo'
          description='Đang chạy ở chế độ demo (không có pywebview)'
          type='info'
          showIcon
          style={{ marginBottom: 24 }}
        />
      )}

      {/* Device Grid */}
      {loading && devices.length === 0 ? (
        <div style={{ textAlign: 'center', padding: 60 }}>
          <Spin size='large' />
          <div style={{ marginTop: 16 }}>
            <Text type='secondary'>Đang tải danh sách thiết bị...</Text>
          </div>
        </div>
      ) : (
        <DeviceGrid
          devices={devices}
          loading={loading}
          onRefresh={handleRefresh}
          onDisconnectAll={handleDisconnectAll}
        />
      )}
    </div>
  );
};

export default MonitoringContent;
