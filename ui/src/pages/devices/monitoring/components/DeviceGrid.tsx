/**
 * DeviceGrid - Grid container for displaying multiple DeviceCards
 *
 * Handles responsive layout and empty state display.
 * Provides controls for refreshing and disconnecting all devices.
 */

import React from 'react';
import { DeviceCard } from './DeviceCard';
import type { Device } from '../types/monitoring.types';
import './DeviceGrid.css';

// =============================================================================
// TYPES
// =============================================================================

interface DeviceGridProps {
  /** Array of devices to display */
  devices: Device[];

  /** Whether currently loading */
  loading?: boolean;

  /** Callback to refresh device list */
  onRefresh?: () => void;

  /** Callback to disconnect all devices */
  onDisconnectAll?: () => void;
}

// =============================================================================
// COMPONENT
// =============================================================================

export const DeviceGrid: React.FC<DeviceGridProps> = ({
  devices,
  loading = false,
  onRefresh,
  onDisconnectAll,
}) => {
  // Count streaming devices
  const streamingCount = devices.filter((d) => d.is_streaming).length;
  const onlineCount = devices.filter((d) => d.is_online).length;

  // =========================================================================
  // RENDER - Empty State
  // =========================================================================

  if (!loading && devices.length === 0) {
    return (
      <div className='device-grid-empty'>
        <div className='empty-icon'>📱</div>
        <h3 className='empty-title'>Không có thiết bị</h3>
        <p className='empty-description'>Kết nối điện thoại Android qua USB và bật USB debugging</p>
        <div className='empty-steps'>
          <div className='step'>
            <span className='step-number'>1</span>
            <span className='step-text'>Vào Settings → About Phone</span>
          </div>
          <div className='step'>
            <span className='step-number'>2</span>
            <span className='step-text'>Nhấn Build Number 7 lần</span>
          </div>
          <div className='step'>
            <span className='step-number'>3</span>
            <span className='step-text'>Vào Developer Options → USB Debugging</span>
          </div>
          <div className='step'>
            <span className='step-number'>4</span>
            <span className='step-text'>Kết nối USB và cho phép trên điện thoại</span>
          </div>
        </div>
        {onRefresh && (
          <button className='empty-refresh-btn' onClick={onRefresh}>
            🔄 Quét lại thiết bị
          </button>
        )}
      </div>
    );
  }

  // =========================================================================
  // RENDER - Grid
  // =========================================================================

  return (
    <div className='device-grid-container'>
      {/* Header with stats */}
      <div className='device-grid-header'>
        <div className='grid-stats'>
          <div className='stat'>
            <span className='stat-value'>{devices.length}</span>
            <span className='stat-label'>Thiết bị</span>
          </div>
          <div className='stat'>
            <span className='stat-value'>{onlineCount}</span>
            <span className='stat-label'>Online</span>
          </div>
          <div className='stat streaming'>
            <span className='stat-value'>{streamingCount}</span>
            <span className='stat-label'>Streaming</span>
          </div>
        </div>

        <div className='grid-actions'>
          {onRefresh && (
            <button
              className='action-btn refresh'
              onClick={onRefresh}
              disabled={loading}
              title='Quét lại thiết bị'
            >
              {loading ? '⏳' : '🔄'} Refresh
            </button>
          )}
          {onDisconnectAll && streamingCount > 0 && (
            <button
              className='action-btn disconnect-all'
              onClick={onDisconnectAll}
              title='Ngắt kết nối tất cả'
            >
              ⏹️ Ngắt tất cả
            </button>
          )}
        </div>
      </div>

      {/* Device grid */}
      <div className='device-grid'>
        {devices.map((device, index) => (
          <DeviceCard
            key={device.device_id}
            device={device}
            index={index + 1}
            onRefresh={onRefresh}
          />
        ))}
      </div>

      {/* Loading overlay */}
      {loading && (
        <div className='grid-loading-overlay'>
          <div className='loading-spinner'>⏳</div>
          <div className='loading-text'>Đang tải...</div>
        </div>
      )}
    </div>
  );
};

export default DeviceGrid;
