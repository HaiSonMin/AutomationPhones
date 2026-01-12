/**
 * TypeScript types for monitoring
 */

export interface Device {
  device_id: string;
  model: string;
  adb_status: string;
  state: 'offline' | 'unauthorized' | 'online' | 'previewing' | 'interactive' | 'error';
  is_online: boolean;
  has_preview: boolean;
  has_window: boolean;
  fps: number;
  error: string | null;
}

export interface GlobalSettings {
  auto_preview?: boolean;
  preview_fps?: number;
  preview_size?: number;
  preview_quality?: number;
  max_size: number;
  max_fps: number;
  bitrate: number;
  fps?: number;
  auto_connect?: boolean;
}

export interface MonitoringStats {
  device_count: number;
  previewing_count: number;
  window_count: number;
  is_running: boolean;
  is_available: boolean;
}

export interface ApiResult {
  success: boolean;
  error?: string;
}

// Event interfaces
export interface DevicesChangedEvent {
  devices: Device[];
}

export interface FrameEvent {
  deviceId: string;
  frame: string; // base64 JPEG
}
