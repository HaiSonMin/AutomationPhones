/**
 * GlobalSettingsModal - Settings popup for monitoring
 */

import React, { useState, useEffect } from 'react';
import { Modal, Slider, Switch, Button, Space, Typography, Divider } from 'antd';
import {
  SettingOutlined,
  ThunderboltOutlined,
  ExpandOutlined,
  SyncOutlined,
} from '@ant-design/icons';
import type { GlobalSettings } from '../types/monitoring.types';

const { Text } = Typography;

interface GlobalSettingsModalProps {
  open: boolean;
  onClose: () => void;
  settings: GlobalSettings;
  onSave: (settings: Partial<GlobalSettings>) => Promise<void>;
  loading?: boolean;
}

export const GlobalSettingsModal: React.FC<GlobalSettingsModalProps> = ({
  open,
  onClose,
  settings,
  onSave,
  loading = false,
}) => {
  const [fps, setFps] = useState(settings.fps);
  const [maxSize, setMaxSize] = useState(settings.max_size);
  const [autoConnect, setAutoConnect] = useState(settings.auto_connect);
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    if (open) {
      setFps(settings.fps);
      setMaxSize(settings.max_size);
      setAutoConnect(settings.auto_connect);
    }
  }, [open, settings]);

  const handleSave = async () => {
    setSaving(true);
    try {
      await onSave({ fps, max_size: maxSize, auto_connect: autoConnect });
      onClose();
    } finally {
      setSaving(false);
    }
  };

  const fpsMarks = { 15: '15', 30: '30', 60: '60' };
  const sizeMarks = { 480: '480', 720: '720', 800: '800', 1080: '1080' };

  return (
    <Modal
      title={
        <Space>
          <SettingOutlined />
          <span>Cài đặt (Low Latency)</span>
        </Space>
      }
      open={open}
      onCancel={onClose}
      footer={[
        <Button key='cancel' onClick={onClose}>
          Hủy
        </Button>,
        <Button key='save' type='primary' onClick={handleSave} loading={saving || loading}>
          Lưu thay đổi
        </Button>,
      ]}
      width={480}
    >
      <div style={{ padding: '8px 0' }}>
        {/* Info banner */}
        <div
          style={{
            background: 'rgba(34, 197, 94, 0.1)',
            padding: 12,
            borderRadius: 8,
            marginBottom: 16,
          }}
        >
          <Text style={{ color: '#22c55e' }}>⚡ Sử dụng scrcpy streaming với latency 35-70ms</Text>
        </div>

        {/* FPS Setting */}
        <div style={{ marginBottom: 24 }}>
          <Space align='center' style={{ marginBottom: 8 }}>
            <ThunderboltOutlined style={{ color: '#f59e0b' }} />
            <Text strong>FPS</Text>
            <Text type='secondary'>: {fps}</Text>
          </Space>
          <Slider min={15} max={60} step={5} marks={fpsMarks} value={fps} onChange={setFps} />
          <Text type='secondary' style={{ fontSize: 12 }}>
            FPS cao hơn = mượt hơn, nhưng tốn CPU hơn
          </Text>
        </div>

        <Divider />

        {/* Size Setting */}
        <div style={{ marginBottom: 24 }}>
          <Space align='center' style={{ marginBottom: 8 }}>
            <ExpandOutlined style={{ color: '#3b82f6' }} />
            <Text strong>Kích thước</Text>
            <Text type='secondary'>: {maxSize}px</Text>
          </Space>
          <Slider
            min={480}
            max={1080}
            step={80}
            marks={sizeMarks}
            value={maxSize}
            onChange={setMaxSize}
          />
        </div>

        <Divider />

        {/* Auto-connect */}
        <div>
          <Space style={{ width: '100%', justifyContent: 'space-between' }}>
            <Space>
              <SyncOutlined style={{ color: '#22c55e' }} />
              <Text strong>Tự động kết nối</Text>
            </Space>
            <Switch
              checked={autoConnect}
              onChange={setAutoConnect}
              checkedChildren='Bật'
              unCheckedChildren='Tắt'
            />
          </Space>
        </div>
      </div>
    </Modal>
  );
};

export default GlobalSettingsModal;
