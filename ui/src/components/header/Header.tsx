import { useState, useEffect } from 'react';
import { Typography, Space, Button, Avatar, Dropdown, Badge, Tooltip } from 'antd';
import {
  UserOutlined,
  LogoutOutlined,
  SettingOutlined,
  BellOutlined,
  MenuFoldOutlined,
  MenuUnfoldOutlined,
  PoweroffOutlined,
  SunOutlined,
  MoonOutlined,
} from '@ant-design/icons';
import type { MenuProps } from 'antd';
import { useThemeStore } from '../../stores/themeStore';

const { Title } = Typography;

interface HeaderProps {
  collapsed?: boolean;
  onToggle?: () => void;
  user?: {
    name: string;
    email: string;
    avatar?: string;
  };
  notifications?: number;
}

const Header: React.FC<HeaderProps> = ({
  collapsed = false,
  onToggle,
  user,
  notifications = 0,
}) => {
  const [currentTime, setCurrentTime] = useState(new Date());
  const [appRunning, setAppRunning] = useState(false);
  const { mode: themeMode, toggleTheme } = useThemeStore();

  const isDark = themeMode === 'dark';

  useEffect(() => {
    const timer = setInterval(() => {
      setCurrentTime(new Date());
    }, 1000);

    return () => clearInterval(timer);
  }, []);

  useEffect(() => {
    // Fetch initial app state
    const fetchAppState = async () => {
      try {
        if (!window.pywebview?.api) {
          console.error('PyWebView API not available');
          return;
        }
        const result = await window.pywebview.api.tools_get_app_state();
        setAppRunning(result.running);
      } catch (error) {
        console.error('Failed to get app state:', error);
      }
    };
    fetchAppState();
  }, []);

  const handleLogout = async () => {
    try {
      if (!window.pywebview?.api) {
        console.error('PyWebView API not available');
        return;
      }
      await window.pywebview.api.auth_on_logout();
      window.location.reload();
    } catch (error) {
      console.error('Logout failed:', error);
    }
  };

  const handleStartStopApp = async () => {
    try {
      if (!window.pywebview?.api) {
        console.error('PyWebView API not available');
        return;
      }
      const result = await window.pywebview.api.tools_start_stop();
      if (result.success) {
        setAppRunning(result.running);
      }
    } catch (error) {
      console.error('Failed to start/stop app:', error);
    }
  };

  const userMenuItems: MenuProps['items'] = [
    {
      key: 'profile',
      icon: <UserOutlined />,
      label: user?.name || 'Guest',
      children: [
        {
          key: 'info',
          label: `Email: ${user?.email || 'N/A'}`,
          disabled: true,
        },
      ],
    },
    {
      key: 'theme',
      icon: isDark ? <SunOutlined /> : <MoonOutlined />,
      label: isDark ? 'Light Mode' : 'Dark Mode',
      onClick: toggleTheme,
    },
    {
      key: 'app_control',
      icon: <PoweroffOutlined />,
      label: appRunning ? 'Stop Tool PC' : 'Start Tool PC',
      onClick: handleStartStopApp,
      danger: appRunning,
    },
    {
      type: 'divider',
    },
    {
      key: 'settings',
      icon: <SettingOutlined />,
      label: 'Settings',
      onClick: () => {
        console.log('Navigate to settings');
      },
    },
    {
      key: 'logout',
      icon: <LogoutOutlined />,
      label: 'Logout',
      onClick: handleLogout,
    },
  ];

  const formatTime = (date: Date) => {
    return date.toLocaleTimeString('vi-VN', {
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit',
    });
  };

  const formatDate = (date: Date) => {
    return date.toLocaleDateString('vi-VN', {
      weekday: 'long',
      year: 'numeric',
      month: 'long',
      day: 'numeric',
    });
  };

  return (
    <div
      style={{
        paddingRight: '24px',
        background: isDark ? '#1f1f1f' : '#fff',
        borderBottom: isDark ? '1px solid #303030' : '1px solid #f0f0f0',
        display: 'flex',
        justifyContent: 'space-between',
        height: '64px',
        boxShadow: isDark ? '0 1px 4px rgba(0,0,0,.3)' : '0 1px 4px rgba(0,21,41,.08)',
      }}
    >
      {/* Left side - Toggle button */}
      <Button
        type='text'
        icon={collapsed ? <MenuUnfoldOutlined /> : <MenuFoldOutlined />}
        onClick={onToggle}
        style={{
          fontSize: '16px',
          width: 64,
          height: 64,
          color: isDark ? '#ffffff' : undefined,
        }}
      />

      {/* Center - Date and Time */}
      <Space direction='vertical' size={0} style={{ textAlign: 'center' }}>
        <Title
          level={5}
          style={{
            margin: 0,
            color: isDark ? '#a0a0a0' : '#666',
            fontSize: '12px',
          }}
        >
          {formatDate(currentTime)}
        </Title>
        <Title level={4} style={{ margin: 0, color: '#1890ff', fontSize: '16px' }}>
          {formatTime(currentTime)}
        </Title>
      </Space>

      {/* Right side - Notifications and User */}
      <Space align='center' size='large'>
        {/* App Status */}
        <Tooltip title={appRunning ? 'Tool PC is running' : 'Tool PC is stopped'}>
          <Space size={4}>
            <Badge status={appRunning ? 'success' : 'default'} />
            <span
              style={{
                color: isDark ? '#a0a0a0' : '#666',
                fontSize: '12px',
              }}
            >
              {appRunning ? 'Running' : 'Stopped'}
            </span>
          </Space>
        </Tooltip>

        {/* Notifications */}
        <Tooltip title='Notifications'>
          <Badge count={notifications} size='small'>
            <Button
              type='text'
              icon={
                <BellOutlined style={{ fontSize: '18px', color: isDark ? '#ffffff' : undefined }} />
              }
              onClick={() => {
                console.log('Show notifications');
              }}
            />
          </Badge>
        </Tooltip>

        {/* User Dropdown */}
        <Dropdown menu={{ items: userMenuItems }} placement='bottomRight'>
          <Space style={{ cursor: 'pointer' }}>
            <Avatar size='small' src={user?.avatar} icon={<UserOutlined />} />
            <span
              style={{
                color: isDark ? '#e0e0e0' : '#666',
                fontSize: '14px',
              }}
            >
              {user?.name || 'Guest'}
            </span>
          </Space>
        </Dropdown>
      </Space>
    </div>
  );
};

export default Header;
