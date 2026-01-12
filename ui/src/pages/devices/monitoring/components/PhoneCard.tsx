/**
 * PhoneCard - Device card with scrcpy window control
 *
 * Scrcpy window only approach (~35-70ms latency)
 */

import React from 'react';
import { Button, Tooltip, Badge, Tag } from 'antd';
import { ExpandOutlined, CloseOutlined, CheckCircleFilled, WarningFilled } from '@ant-design/icons';
import type { Device } from '../types/monitoring.types';
import './PhoneCard.css';

interface PhoneCardProps {
  device: Device;
  index: number;
  onOpenWindow: (deviceId: string) => void;
  onCloseWindow: (deviceId: string) => void;
}

export const PhoneCard: React.FC<PhoneCardProps> = ({
  device,
  index,
  onOpenWindow,
  onCloseWindow,
}) => {
  const getStatusIcon = () => {
    if (device.has_window) return <CheckCircleFilled style={{ color: '#22c55e' }} />;
    if (device.state === 'online') return <Badge status='processing' />;
    if (device.state === 'unauthorized') return <WarningFilled style={{ color: '#f59e0b' }} />;
    return <Badge status='default' />;
  };

  const getStatusTag = () => {
    if (device.has_window) return <Tag color='green'>Window Open</Tag>;
    if (device.state === 'online') return <Tag color='blue'>Online</Tag>;
    if (device.state === 'unauthorized') return <Tag color='orange'>Unauthorized</Tag>;
    return <Tag>Offline</Tag>;
  };

  return (
    <div
      className={`phone-card-compact ${device.has_window ? 'active' : ''} ${
        !device.is_online ? 'offline' : ''
      }`}
    >
      <div className='phone-card-compact-left'>
        <div className='phone-card-compact-index'>{String(index).padStart(2, '0')}</div>
        {getStatusIcon()}
      </div>

      <div className='phone-card-compact-info'>
        <div className='phone-card-compact-model'>{device.model}</div>
        <div className='phone-card-compact-id'>{device.device_id}</div>
        <div className='phone-card-compact-status'>{getStatusTag()}</div>
      </div>

      <div className='phone-card-compact-actions'>
        {device.has_window ? (
          <Tooltip title='Đóng scrcpy window'>
            <Button
              type='primary'
              danger
              icon={<CloseOutlined />}
              onClick={() => onCloseWindow(device.device_id)}
            >
              Đóng
            </Button>
          </Tooltip>
        ) : device.is_online ? (
          <Tooltip title='Mở scrcpy window (~35-70ms latency)'>
            <Button
              type='primary'
              icon={<ExpandOutlined />}
              onClick={() => onOpenWindow(device.device_id)}
            >
              Mở Window
            </Button>
          </Tooltip>
        ) : (
          <Button disabled>Offline</Button>
        )}
      </div>
    </div>
  );
};

export default PhoneCard;
