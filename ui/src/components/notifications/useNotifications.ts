import { useState, useEffect, useCallback } from 'react';
import type { Notification } from './Notifications';

const mockNotifications: Notification[] = [
  // Task notifications
  {
    id: '1',
    type: 'task',
    title: 'Phone Setup Completed',
    message: 'Device Galaxy S21 has been successfully set up',
    timestamp: new Date(Date.now() - 1000 * 60 * 5), // 5 minutes ago
    read: false,
    priority: 'high',
    action: {
      label: 'View Device',
      onClick: () => console.log('Navigate to device'),
    },
  },
  {
    id: '2',
    type: 'task',
    title: 'App Clone Progress',
    message: 'Instagram cloning: 75% completed',
    timestamp: new Date(Date.now() - 1000 * 60 * 30), // 30 minutes ago
    read: false,
    priority: 'medium',
    action: {
      label: 'View Progress',
      onClick: () => console.log('Navigate to progress'),
    },
  },
  {
    id: '3',
    type: 'task',
    title: 'Threads Post Scheduled',
    message: 'Your post has been scheduled for 3:00 PM',
    timestamp: new Date(Date.now() - 1000 * 60 * 60), // 1 hour ago
    read: true,
    priority: 'low',
  },
  {
    id: '4',
    type: 'task',
    title: 'Instagram Story Failed',
    message: 'Failed to upload story. Please check your connection',
    timestamp: new Date(Date.now() - 1000 * 60 * 60 * 2), // 2 hours ago
    read: false,
    priority: 'high',
    action: {
      label: 'Retry',
      onClick: () => console.log('Retry upload'),
    },
  },
  // System notifications
  {
    id: '5',
    type: 'system',
    title: 'System Update Available',
    message: 'Version 2.1.0 is ready to install',
    timestamp: new Date(Date.now() - 1000 * 60 * 60 * 3), // 3 hours ago
    read: true,
    priority: 'medium',
    action: {
      label: 'Update Now',
      onClick: () => console.log('Start update'),
    },
  },
  {
    id: '6',
    type: 'system',
    title: 'Device Connected',
    message: 'New device detected: iPhone 13 Pro',
    timestamp: new Date(Date.now() - 1000 * 60 * 60 * 4), // 4 hours ago
    read: true,
    priority: 'low',
  },
  {
    id: '7',
    type: 'system',
    title: 'Storage Warning',
    message: 'Storage space is running low (85% used)',
    timestamp: new Date(Date.now() - 1000 * 60 * 60 * 5), // 5 hours ago
    read: false,
    priority: 'high',
    action: {
      label: 'Manage Storage',
      onClick: () => console.log('Open storage management'),
    },
  },
  {
    id: '8',
    type: 'system',
    title: 'Backup Completed',
    message: 'Your data has been successfully backed up',
    timestamp: new Date(Date.now() - 1000 * 60 * 60 * 24), // 1 day ago
    read: true,
    priority: 'low',
  },
];

export const useNotifications = () => {
  const [notifications, setNotifications] = useState<Notification[]>(mockNotifications);
  const [loading, setLoading] = useState(false);
  const [hasMore, setHasMore] = useState(true);

  // Simulate loading more notifications
  const loadMore = useCallback(() => {
    if (loading || !hasMore) return;

    setLoading(true);

    // Simulate API call
    setTimeout(() => {
      const moreNotifications: Notification[] = Array.from({ length: 5 }, (_, i) => ({
        id: `more-${notifications.length + i}`,
        type: Math.random() > 0.5 ? 'task' : 'system',
        title: `Old Notification ${notifications.length + i + 1}`,
        message: 'This is an older notification loaded from infinite scroll',
        timestamp: new Date(Date.now() - 1000 * 60 * 60 * 24 * (notifications.length + i + 2)),
        read: true,
        priority: 'low',
      }));

      setNotifications((prev) => [...prev, ...moreNotifications]);
      setLoading(false);

      // Stop loading more after 3 batches
      if (notifications.length > 15) {
        setHasMore(false);
      }
    }, 1000);
  }, [loading, hasMore, notifications.length]);

  const markAsRead = useCallback((id: string) => {
    setNotifications((prev) => prev.map((n) => (n.id === id ? { ...n, read: true } : n)));
  }, []);

  const markAllAsRead = useCallback(() => {
    setNotifications((prev) => prev.map((n) => ({ ...n, read: true })));
  }, []);

  const deleteNotification = useCallback((id: string) => {
    setNotifications((prev) => prev.filter((n) => n.id !== id));
  }, []);

  const clearAll = useCallback(() => {
    setNotifications([]);
    setHasMore(false);
  }, []);

  // Simulate receiving new notifications
  useEffect(() => {
    const interval = setInterval(() => {
      const newNotification: Notification = {
        id: `new-${Date.now()}`,
        type: Math.random() > 0.5 ? 'task' : 'system',
        title: 'New Activity',
        message: 'Something new happened in your system',
        timestamp: new Date(),
        read: false,
        priority: Math.random() > 0.7 ? 'high' : Math.random() > 0.3 ? 'medium' : 'low',
      };

      setNotifications((prev) => [newNotification, ...prev.slice(0, 49)]);
    }, 30000); // Every 30 seconds

    return () => clearInterval(interval);
  }, []);

  return {
    notifications,
    loading,
    hasMore,
    loadMore,
    markAsRead,
    markAllAsRead,
    deleteNotification,
    clearAll,
  };
};
