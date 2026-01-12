/**
 * MonitoringContent - Main content for monitoring
 *
 * Scrcpy window only approach (~35-70ms latency)
 */

import React, { useState, useEffect, useCallback } from 'react';
import { Typography, Spin, Alert, Button, Row, Col, Statistic, Card, Tooltip, message } from 'antd';
import {
  SettingOutlined,
  MobileOutlined,
  ReloadOutlined,
  DesktopOutlined,
} from '@ant-design/icons';
import { PhoneCard } from './components/PhoneCard';
import { GlobalSettingsModal } from './components/GlobalSettingsModal';
import { useMonitoringBridge } from './hooks/useMonitoringBridge';
import { useDeviceEvents } from './hooks/useDeviceEvents';
import type { Device, GlobalSettings } from './types/monitoring.types';
import './MonitoringPage.css';

const { Title, Text } = Typography;

const DEFAULT_SETTINGS: GlobalSettings = {
  max_size: 800,
  max_fps: 60,
  bitrate: 8,
};

export const MonitoringContent: React.FC = () => {
  const bridge = useMonitoringBridge();

  const [devices, setDevices] = useState<Device[]>([]);
  const [settings, setSettings] = useState<GlobalSettings>(DEFAULT_SETTINGS);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [settingsOpen, setSettingsOpen] = useState(false);

  const loadData = useCallback(
    async (forceRefresh = false) => {
      try {
        setLoading(true);
        setError(null);

        const [devicesData, settingsData] = await Promise.all([
          forceRefresh ? bridge.refreshDevices() : bridge.getDevices(),
          bridge.getSettings(),
        ]);

        setDevices(devicesData);
        setSettings(settingsData);
      } catch (err) {
        setError(String(err));
      } finally {
        setLoading(false);
      }
    },
    [bridge]
  );

  useEffect(() => {
    loadData();
  }, [loadData]);

  const handleDevicesChanged = useCallback((newDevices: Device[]) => {
    setDevices(newDevices);
  }, []);

  useDeviceEvents(handleDevicesChanged, undefined, true);

  const handleOpenWindow = async (deviceId: string) => {
    const result = await bridge.openWindow(deviceId);
    if (result.success) {
      message.success('Đang mở scrcpy window...');
    } else {
      message.error(result.error || 'Failed to open window');
    }
  };

  const handleCloseWindow = async (deviceId: string) => {
    await bridge.closeWindow(deviceId);
  };

  const handleStopAll = async () => {
    await bridge.stopAll();
    message.info('Đã đóng tất cả windows');
  };

  const handleSaveSettings = async (newSettings: Partial<GlobalSettings>) => {
    const updated = await bridge.updateSettings(newSettings);
    setSettings(updated);
    message.success('Đã lưu cài đặt');
  };

  const onlineCount = devices.filter((d) => d.is_online).length;
  const windowCount = devices.filter((d) => d.has_window).length;

  if (loading) {
    return (
      <div className='monitoring-loading'>
        <Spin size='large' />
        <Text type='secondary'>Đang tải...</Text>
      </div>
    );
  }

  if (error) {
    return (
      <Alert
        type='error'
        message='Lỗi'
        description={error}
        action={<Button onClick={() => loadData(true)}>Thử lại</Button>}
      />
    );
  }

  return (
    <div className='monitoring-container'>
      {/* Header */}
      <div className='monitoring-header'>
        <div className='header-left'>
          <Title level={3} style={{ margin: 0 }}>
            ⚡ Monitoring
          </Title>
          <Text type='secondary'>Scrcpy window (~35-70ms latency)</Text>
        </div>
        <div className='header-right'>
          <Tooltip title='Đóng tất cả'>
            <Button onClick={handleStopAll}>Stop All</Button>
          </Tooltip>
          <Tooltip title='Làm mới'>
            <Button icon={<ReloadOutlined />} onClick={() => loadData(true)} />
          </Tooltip>
          <Tooltip title='Cài đặt'>
            <Button icon={<SettingOutlined />} onClick={() => setSettingsOpen(true)} />
          </Tooltip>
        </div>
      </div>

      {/* Stats */}
      <Row gutter={16} className='monitoring-stats'>
        <Col span={8}>
          <Card size='small'>
            <Statistic title='Thiết bị' value={devices.length} prefix={<MobileOutlined />} />
          </Card>
        </Col>
        <Col span={8}>
          <Card size='small'>
            <Statistic title='Online' value={onlineCount} valueStyle={{ color: '#22c55e' }} />
          </Card>
        </Col>
        <Col span={8}>
          <Card size='small'>
            <Statistic
              title='Windows'
              value={windowCount}
              valueStyle={{ color: '#f59e0b' }}
              prefix={<DesktopOutlined />}
            />
          </Card>
        </Col>
      </Row>

      {/* Device List */}
      {devices.length === 0 ? (
        <div className='monitoring-empty'>
          <MobileOutlined style={{ fontSize: 64, opacity: 0.3 }} />
          <Text type='secondary'>Không có thiết bị nào được kết nối</Text>
          <Text type='secondary' style={{ fontSize: 12 }}>
            Cắm điện thoại Android qua USB và bật USB Debugging
          </Text>
        </div>
      ) : (
        <div className='monitoring-list'>
          {devices.map((device, index) => (
            <>
              <PhoneCard
                key={device.device_id}
                device={device}
                index={index + 1}
                onOpenWindow={handleOpenWindow}
                onCloseWindow={handleCloseWindow}
              />
            </>
          ))}
        </div>
      )}

      {/* Settings Modal */}
      <GlobalSettingsModal
        open={settingsOpen}
        onClose={() => setSettingsOpen(false)}
        settings={settings}
        onSave={handleSaveSettings}
      />
    </div>
  );
};

export default MonitoringContent;
