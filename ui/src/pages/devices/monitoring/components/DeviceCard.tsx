/**
 * DeviceCard - Display and control a single Android device
 *
 * Shows device info, streaming status, FPS/size controls, and connect/disconnect button.
 * This component handles user interactions and calls the bridge API.
 *
 * Features:
 * - Display device model and status
 * - FPS slider (5-60)
 * - Size slider (480-1440)
 * - Connect/Disconnect button
 * - Error display
 */

import React, { useState, useCallback, useMemo } from 'react';
import { useMonitoringBridge } from '../hooks/useMonitoringBridge';
import VideoDisplay from './VideoDisplay';
import type { Device, DeviceState } from '../types/monitoring.types';
import './DeviceCard.css';

// =============================================================================
// TYPES
// =============================================================================

interface DeviceCardProps {
  /** Device data from bridge */
  device: Device;

  /** Display index (1-based, for UI label) */
  index: number;

  /** Callback to refresh device list after changes */
  onRefresh?: () => void;
}

// =============================================================================
// HELPERS
// =============================================================================

/**
 * Get display label and color for device state
 */
function getStateDisplay(state: DeviceState): { label: string; color: string } {
  const stateMap: Record<DeviceState, { label: string; color: string }> = {
    disconnected: { label: 'Ngắt kết nối', color: '#666' },
    unauthorized: { label: 'Chưa cấp quyền', color: '#f59e0b' },
    offline: { label: 'Offline', color: '#6b7280' },
    online: { label: 'Sẵn sàng', color: '#10b981' },
    connecting: { label: 'Đang kết nối...', color: '#3b82f6' },
    streaming: { label: 'Đang stream', color: '#22c55e' },
    error: { label: 'Lỗi', color: '#ef4444' },
  };

  return stateMap[state] || { label: state, color: '#666' };
}

/**
 * Get status icon based on state
 */
function getStateIcon(state: DeviceState): string {
  const iconMap: Record<DeviceState, string> = {
    disconnected: '📴',
    unauthorized: '🔐',
    offline: '📵',
    online: '📱',
    connecting: '⏳',
    streaming: '🎬',
    error: '❌',
  };

  return iconMap[state] || '❓';
}

// =============================================================================
// COMPONENT
// =============================================================================

export const DeviceCard: React.FC<DeviceCardProps> = ({ device, index, onRefresh }) => {
  const bridge = useMonitoringBridge();

  // Local state for loading and settings
  const [loading, setLoading] = useState(false);
  const [localFps, setLocalFps] = useState(device.fps);
  const [localSize, setLocalSize] = useState(device.max_size);

  // Derived state
  const isStreaming = device.state === 'streaming';
  const canConnect = device.can_connect;
  const stateDisplay = useMemo(() => getStateDisplay(device.state), [device.state]);

  // =========================================================================
  // HANDLERS
  // =========================================================================

  /**
   * Handle connect button click
   */
  const handleConnect = useCallback(async () => {
    if (loading) return;

    setLoading(true);
    try {
      const result = await bridge.connect(device.device_id);

      if (!result.success) {
        console.error('Connect failed:', result.error);
        // Could show toast notification here
      }

      onRefresh?.();
    } catch (error) {
      console.error('Connect error:', error);
    } finally {
      setLoading(false);
    }
  }, [bridge, device.device_id, loading, onRefresh]);

  /**
   * Handle disconnect button click
   */
  const handleDisconnect = useCallback(async () => {
    if (loading) return;

    setLoading(true);
    try {
      const result = await bridge.disconnect(device.device_id);

      if (!result.success) {
        console.error('Disconnect failed:', result.error);
      }

      onRefresh?.();
    } catch (error) {
      console.error('Disconnect error:', error);
    } finally {
      setLoading(false);
    }
  }, [bridge, device.device_id, loading, onRefresh]);

  /**
   * Handle FPS slider change
   */
  const handleFpsChange = useCallback(
    async (newFps: number) => {
      setLocalFps(newFps);

      // Only call API if streaming (otherwise just save for later)
      if (isStreaming) {
        const result = await bridge.setFps(device.device_id, newFps);
        if (!result.success) {
          console.error('Set FPS failed:', result.error);
          // Revert on error
          setLocalFps(device.fps);
        }
        onRefresh?.();
      }
    },
    [bridge, device.device_id, device.fps, isStreaming, onRefresh]
  );

  /**
   * Handle size slider change
   */
  const handleSizeChange = useCallback(
    async (newSize: number) => {
      setLocalSize(newSize);

      // Only call API if streaming (otherwise just save for later)
      if (isStreaming) {
        const result = await bridge.setSize(device.device_id, newSize);
        if (!result.success) {
          console.error('Set size failed:', result.error);
          // Revert on error
          setLocalSize(device.max_size);
        }
        onRefresh?.();
      }
    },
    [bridge, device.device_id, device.max_size, isStreaming, onRefresh]
  );

  // =========================================================================
  // RENDER
  // =========================================================================

  return (
    <div className={`device-card ${device.state}`}>
      {/* ===== Header ===== */}
      <div className='device-card-header'>
        {/* Index badge */}
        <div className='device-index'>{String(index).padStart(2, '0')}</div>

        {/* Device info */}
        <div className='device-info'>
          <div className='device-model'>{device.model}</div>
          <div className='device-id' title={device.device_id}>
            {device.device_id.length > 12
              ? `${device.device_id.slice(0, 12)}...`
              : device.device_id}
          </div>
        </div>

        {/* Status indicator */}
        <div
          className='device-status'
          style={{ backgroundColor: stateDisplay.color }}
          title={stateDisplay.label}
        >
          <span className='status-icon'>{getStateIcon(device.state)}</span>
        </div>
      </div>

      {/* ===== Screen placeholder ===== */}
      <div className='device-screen'>
        {isStreaming ? (
          <VideoDisplay
            deviceId={device.device_id}
            deviceName={device.model || `Device ${index}`}
            isActive={isStreaming}
            onConnect={handleConnect}
            onDisconnect={handleDisconnect}
          />
        ) : device.state === 'unauthorized' ? (
          <div className='screen-unauthorized'>
            <div className='unauthorized-icon'>🔐</div>
            <div className='unauthorized-text'>Chưa cấp quyền</div>
            <div className='unauthorized-hint'>Cho phép USB debugging trên điện thoại</div>
          </div>
        ) : device.state === 'error' ? (
          <div className='screen-error'>
            <div className='error-icon'>❌</div>
            <div className='error-text'>Lỗi</div>
            <div className='error-message'>{device.error || 'Unknown error'}</div>
          </div>
        ) : canConnect ? (
          <div className='screen-ready'>
            <div className='ready-icon'>📱</div>
            <div className='ready-text'>Sẵn sàng</div>
            <div className='ready-hint'>Nhấn Connect để bắt đầu</div>
          </div>
        ) : (
          <div className='screen-offline'>
            <div className='offline-icon'>📵</div>
            <div className='offline-text'>Offline</div>
            <div className='offline-hint'>Kiểm tra kết nối USB</div>
          </div>
        )}
      </div>

      {/* ===== Controls ===== */}
      {!isStreaming && (
        <div className='device-controls'>
          {/* FPS Slider */}
          <div className='control-row'>
            <label className='control-label'>
              FPS: <span className='control-value'>{localFps}</span>
            </label>
            <input
              type='range'
              className='control-slider'
              min={5}
              max={60}
              step={5}
              value={localFps}
              onChange={(e) => handleFpsChange(Number(e.target.value))}
              disabled={device.state === 'connecting'}
            />
          </div>

          {/* Size Slider */}
          <div className='control-row'>
            <label className='control-label'>
              Kích thước: <span className='control-value'>{localSize}px</span>
            </label>
            <input
              type='range'
              className='control-slider'
              min={480}
              max={1440}
              step={80}
              value={localSize}
              onChange={(e) => handleSizeChange(Number(e.target.value))}
              disabled={device.state === 'connecting'}
            />
          </div>

          {/* Connect Button */}
          <button
            className='control-button btn-primary'
            onClick={handleConnect}
            disabled={loading || !canConnect}
          >
            {loading ? (
              <>
                <span className='btn-spinner'>⏳</span>
                <span>Đang xử lý...</span>
              </>
            ) : (
              <>
                <span className='btn-icon'>▶️</span>
                <span>Kết nối</span>
              </>
            )}
          </button>
        </div>
      )}
    </div>
  );
};

export default DeviceCard;
