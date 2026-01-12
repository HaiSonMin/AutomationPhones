import React, { useState, useRef } from 'react';
import { Badge, Button, Dropdown, Typography, Spin, Empty } from 'antd';
import {
  BellOutlined,
  CheckOutlined,
  DeleteOutlined,
  SettingOutlined,
  CheckSquareOutlined,
  SyncOutlined,
  InfoCircleOutlined,
  WarningOutlined,
  CheckCircleOutlined,
  CloseCircleOutlined,
} from '@ant-design/icons';
import { useThemeStore } from '../../stores/themeStore';
import dayjs from 'dayjs';
import relativeTime from 'dayjs/plugin/relativeTime';
import 'dayjs/locale/en';

dayjs.extend(relativeTime);
dayjs.locale('en');

const { Text } = Typography;

export interface Notification {
  id: string;
  type: 'task' | 'system';
  title: string;
  message: string;
  timestamp: Date;
  read: boolean;
  icon?: React.ReactNode;
  priority?: 'low' | 'medium' | 'high';
  action?: {
    label: string;
    onClick: () => void;
  };
}

interface NotificationsProps {
  notifications: Notification[];
  onMarkAsRead: (id: string) => void;
  onMarkAllAsRead: () => void;
  onDelete: (id: string) => void;
  onClearAll: () => void;
  onLoadMore?: () => void;
  hasMore?: boolean;
  loading?: boolean;
}

const Notifications: React.FC<NotificationsProps> = ({
  notifications,
  onMarkAsRead,
  onMarkAllAsRead,
  onDelete,
  onClearAll,
  onLoadMore,
  hasMore = false,
  loading = false,
}) => {
  const [open, setOpen] = useState(false);
  const themeMode = useThemeStore((state) => state.mode);
  const isDark = themeMode === 'dark';
  const scrollRef = useRef<HTMLDivElement>(null);

  const unreadCount = notifications.filter((n) => !n.read).length;

  const getNotificationIcon = (notification: Notification) => {
    if (notification.icon) return notification.icon;

    if (notification.type === 'task') {
      switch (notification.priority) {
        case 'high':
          return <WarningOutlined style={{ color: '#ff4d4f' }} />;
        case 'medium':
          return <InfoCircleOutlined style={{ color: '#1890ff' }} />;
        default:
          return <CheckSquareOutlined style={{ color: '#52c41a' }} />;
      }
    } else {
      switch (notification.priority) {
        case 'high':
          return <CloseCircleOutlined style={{ color: '#ff4d4f' }} />;
        case 'medium':
          return <SyncOutlined style={{ color: '#faad14' }} />;
        default:
          return <CheckCircleOutlined style={{ color: '#52c41a' }} />;
      }
    }
  };

  const handleScroll = (e: React.UIEvent<HTMLDivElement>) => {
    const { scrollTop, scrollHeight, clientHeight } = e.currentTarget;
    if (scrollHeight - scrollTop <= clientHeight + 50 && hasMore && !loading && onLoadMore) {
      onLoadMore();
    }
  };

  const NotificationItem: React.FC<{ notification: Notification }> = ({ notification }) => {
    const isUnread = !notification.read;

    return (
      <div
        className={`notification-item ${isUnread ? 'unread' : ''}`}
        style={{
          padding: '12px 16px',
          backgroundColor: isUnread ? (isDark ? '#262626' : '#f6ffed') : 'transparent',
          cursor: 'pointer',
          transition: 'all 0.2s',
          borderBottom: `1px solid ${isDark ? '#303030' : '#f0f0f0'}`,
        }}
        onClick={() => {
          if (isUnread) onMarkAsRead(notification.id);
          notification.action?.onClick();
        }}
      >
        <div style={{ display: 'flex', gap: '12px' }}>
          <div style={{ fontSize: '20px', marginTop: '2px' }}>
            {getNotificationIcon(notification)}
          </div>
          <div style={{ flex: 1, minWidth: 0 }}>
            <div
              style={{
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'flex-start',
                marginBottom: '4px',
              }}
            >
              <Text
                strong={isUnread}
                style={{
                  fontSize: '14px',
                  color: isDark ? '#ffffff' : '#262626',
                  display: 'block',
                  overflow: 'hidden',
                  textOverflow: 'ellipsis',
                  whiteSpace: 'nowrap',
                  maxWidth: '200px',
                }}
              >
                {notification.title}
              </Text>
              <Button
                type='text'
                size='small'
                icon={<DeleteOutlined />}
                onClick={(e) => {
                  e.stopPropagation();
                  onDelete(notification.id);
                }}
                style={{
                  padding: '0 4px',
                  opacity: 0.6,
                }}
              />
            </div>
            <Text
              style={{
                fontSize: '13px',
                color: isDark ? '#a0a0a0' : '#8c8c8c',
                display: 'block',
                marginBottom: '4px',
                overflow: 'hidden',
                textOverflow: 'ellipsis',
                whiteSpace: 'nowrap',
              }}
            >
              {notification.message}
            </Text>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <Text
                style={{
                  fontSize: '12px',
                  color: isDark ? '#737373' : '#bfbfbf',
                }}
              >
                {dayjs(notification.timestamp).fromNow()}
              </Text>
              {notification.action && (
                <Button
                  type='link'
                  size='small'
                  onClick={(e) => {
                    e.stopPropagation();
                    notification.action!.onClick();
                  }}
                  style={{
                    padding: '0',
                    height: 'auto',
                    fontSize: '12px',
                  }}
                >
                  {notification.action.label}
                </Button>
              )}
            </div>
          </div>
        </div>
      </div>
    );
  };

  const headerContent = (
    <div
      style={{
        padding: '12px 16px',
        borderBottom: `1px solid ${isDark ? '#303030' : '#f0f0f0'}`,
        backgroundColor: isDark ? '#1f1f1f' : '#ffffff',
      }}
    >
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <Text strong style={{ fontSize: '16px', color: isDark ? '#ffffff' : '#262626' }}>
          Notifications
        </Text>
        <div style={{ display: 'flex', gap: '8px' }}>
          {unreadCount > 0 && (
            <Button
              type='text'
              size='small'
              icon={<CheckOutlined />}
              onClick={() => onMarkAllAsRead()}
              style={{ fontSize: '12px' }}
            >
              Mark all read
            </Button>
          )}
          <Button type='text' size='small' icon={<SettingOutlined />} style={{ fontSize: '12px' }}>
            Settings
          </Button>
        </div>
      </div>
    </div>
  );

  const content = (
    <div
      style={{
        width: '380px',
        maxHeight: '480px',
        backgroundColor: isDark ? '#1f1f1f' : '#ffffff',
        borderRadius: '8px',
        boxShadow: isDark
          ? '0 6px 16px 0 rgba(0, 0, 0, 0.4), 0 3px 6px -4px rgba(0, 0, 0, 0.4)'
          : '0 6px 16px 0 rgba(0, 0, 0, 0.08), 0 3px 6px -4px rgba(0, 0, 0, 0.12)',
        overflow: 'hidden',
      }}
    >
      {headerContent}

      <div
        ref={scrollRef}
        onScroll={handleScroll}
        style={{
          maxHeight: '360px',
          overflowY: 'auto',
        }}
      >
        {notifications.length === 0 ? (
          <div style={{ padding: '40px 20px', textAlign: 'center' }}>
            <Empty
              image={Empty.PRESENTED_IMAGE_SIMPLE}
              description={
                <Text style={{ color: isDark ? '#a0a0a0' : '#8c8c8c' }}>No notifications</Text>
              }
            />
          </div>
        ) : (
          <>
            {notifications.map((notification) => (
              <NotificationItem key={notification.id} notification={notification} />
            ))}
            {hasMore && (
              <div style={{ padding: '16px', textAlign: 'center' }}>
                <Spin size='small' />
                <Text
                  style={{
                    marginLeft: '8px',
                    fontSize: '12px',
                    color: isDark ? '#a0a0a0' : '#8c8c8c',
                  }}
                >
                  Loading more...
                </Text>
              </div>
            )}
          </>
        )}
      </div>

      {notifications.length > 0 && (
        <div
          style={{
            padding: '8px 16px',
            borderTop: `1px solid ${isDark ? '#303030' : '#f0f0f0'}`,
            backgroundColor: isDark ? '#1f1f1f' : '#ffffff',
          }}
        >
          <Button
            type='link'
            size='small'
            onClick={() => onClearAll()}
            style={{ width: '100%', fontSize: '12px' }}
          >
            Clear all notifications
          </Button>
        </div>
      )}
    </div>
  );

  return (
    <Dropdown
      dropdownRender={() => content}
      trigger={['click']}
      open={open}
      onOpenChange={setOpen}
      placement='bottomRight'
      overlayStyle={{ padding: '0' }}
    >
      <Badge count={unreadCount} size='small' offset={[-2, 2]}>
        <Button
          type='text'
          icon={
            <BellOutlined style={{ fontSize: '18px', color: isDark ? '#ffffff' : undefined }} />
          }
          style={{
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            width: '40px',
            height: '40px',
            borderRadius: '50%',
            transition: 'all 0.2s',
          }}
        />
      </Badge>
    </Dropdown>
  );
};

export default Notifications;
