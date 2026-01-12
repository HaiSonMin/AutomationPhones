/**
 * useDeviceEvents - Hook for listening to device and frame events
 */

import { useEffect, useCallback } from 'react';
import type { Device } from '../types/monitoring.types';

export type DevicesChangedCallback = (devices: Device[]) => void;
export type FrameCallback = (deviceId: string, frame: string) => void;

interface DevicesChangedEventDetail {
  devices: Device[];
}

interface FrameEventDetail {
  deviceId: string;
  frame: string;
}

export function useDeviceEvents(
  onDevicesChanged: DevicesChangedCallback,
  onFrame?: FrameCallback,
  enabled: boolean = true
): void {
  const handleDevicesChanged = useCallback(
    (event: Event) => {
      const customEvent = event as CustomEvent<DevicesChangedEventDetail>;
      const devices = customEvent.detail?.devices;
      if (Array.isArray(devices)) {
        onDevicesChanged(devices);
      }
    },
    [onDevicesChanged]
  );

  const handleFrame = useCallback(
    (event: Event) => {
      const customEvent = event as CustomEvent<FrameEventDetail>;
      const { deviceId, frame } = customEvent.detail || {};
      if (deviceId && frame && onFrame) {
        onFrame(deviceId, frame);
      }
    },
    [onFrame]
  );

  useEffect(() => {
    if (!enabled) return;

    window.addEventListener('monitoring-devices-changed', handleDevicesChanged);
    window.addEventListener('monitoring-frame', handleFrame);

    console.log('[useDeviceEvents] Listeners attached');

    return () => {
      window.removeEventListener('monitoring-devices-changed', handleDevicesChanged);
      window.removeEventListener('monitoring-frame', handleFrame);
    };
  }, [enabled, handleDevicesChanged, handleFrame]);
}

export default useDeviceEvents;
