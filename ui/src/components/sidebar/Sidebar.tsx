import {
  CloudDownloadOutlined,
  DashboardOutlined,
  MobileOutlined,
  ReloadOutlined,
} from '@ant-design/icons';
import { Badge, Button, Menu, Modal, Typography } from 'antd';
import React, { useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { useThemeStore } from '../../stores/themeStore';
import { useUpdateCheck } from '../../hooks/useUpdateCheck';
import { updateService } from '../../services/updateService';

const { Paragraph, Text } = Typography;

interface SidebarProps {
  collapsed: boolean;
}

const Sidebar: React.FC<SidebarProps> = ({ collapsed: _collapsed }) => {
  const navigate = useNavigate();
  const location = useLocation();
  const { mode: themeMode } = useThemeStore();
  const { hasUpdate, updateInfo, isChecking, checkForUpdates, currentVersion } = useUpdateCheck();

  const [isUpdateModalOpen, setIsUpdateModalOpen] = useState(false);
  const [isInstalling, setIsInstalling] = useState(false);

  const isDark = themeMode === 'dark';

  const menuItems = [
    {
      key: '/dashboard',
      icon: <DashboardOutlined />,
      label: 'Dashboard',
    },
    {
      key: '/devices',
      icon: <MobileOutlined />,
      label: 'Devices',
      children: [
        {
          key: '/devices/table',
          label: 'Devices',
        },
        {
          key: '/devices/monitor',
          label: 'Device monitoring',
        },
      ],
    },
  ];

  const handleMenuClick = ({ key }: { key: string }) => {
    navigate(key);
  };

  const handleUpdateClick = () => {
    setIsUpdateModalOpen(true);
  };

  const handleInstallUpdate = async () => {
    if (!updateInfo?.download_url) return;

    setIsInstalling(true);
    try {
      const response = await updateService.downloadAndInstall(updateInfo.download_url);

      if (response.success) {
        Modal.success({
          title: 'Update Installing',
          content: 'The application will restart shortly...',
        });
        // App will restart automatically
      } else {
        Modal.error({
          title: 'Update Failed',
          content: response.error || 'Failed to install update',
        });
      }
    } catch (error) {
      Modal.error({
        title: 'Update Error',
        content: String(error),
      });
    } finally {
      setIsInstalling(false);
      setIsUpdateModalOpen(false);
    }
  };

  return (
    <div style={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
      <Menu
        mode='inline'
        theme={isDark ? 'dark' : 'light'}
        selectedKeys={[location.pathname]}
        defaultOpenKeys={['/devices']}
        items={menuItems}
        onClick={handleMenuClick}
        style={{
          flex: 1,
          borderRight: 0,
          paddingTop: '16px',
          background: isDark ? '#1f1f1f' : '#ffffff',
        }}
      />

      {/* Update Section */}
      <div
        style={{
          padding: '16px',
          borderTop: isDark ? '1px solid rgba(255, 255, 255, 0.1)' : '1px solid #f0f0f0',
        }}
      >
        {hasUpdate ? (
          <Badge dot>
            <Button
              type='primary'
              icon={<CloudDownloadOutlined />}
              onClick={handleUpdateClick}
              block
            >
              Update Available
            </Button>
          </Badge>
        ) : (
          <Button
            icon={<ReloadOutlined spin={isChecking} />}
            onClick={checkForUpdates}
            loading={isChecking}
            block
          >
            Check Updates
          </Button>
        )}

        <Text type='secondary' style={{ display: 'block', marginTop: '8px', fontSize: '12px' }}>
          v{currentVersion}
        </Text>
      </div>

      {/* Update Modal */}
      <Modal
        title='Update Available'
        open={isUpdateModalOpen}
        onCancel={() => setIsUpdateModalOpen(false)}
        footer={[
          <Button key='cancel' onClick={() => setIsUpdateModalOpen(false)}>
            Later
          </Button>,
          <Button
            key='install'
            type='primary'
            loading={isInstalling}
            onClick={handleInstallUpdate}
            icon={<CloudDownloadOutlined />}
          >
            Download & Install
          </Button>,
        ]}
      >
        {updateInfo && (
          <div>
            <Paragraph>
              <Text strong>Current Version:</Text> v{updateInfo.current_version}
            </Paragraph>
            <Paragraph>
              <Text strong>New Version:</Text> v{updateInfo.latest_version}
            </Paragraph>
            <Paragraph>
              <Text strong>Changelog:</Text>
            </Paragraph>
            <Paragraph
              style={{
                background: '#f5f5f5',
                padding: '12px',
                borderRadius: '4px',
                maxHeight: '200px',
                overflow: 'auto',
              }}
            >
              {updateInfo.changelog}
            </Paragraph>
            <Paragraph type='warning' style={{ marginTop: '16px' }}>
              ⚠️ The application will restart after the update is installed.
            </Paragraph>
          </div>
        )}
      </Modal>
    </div>
  );
};

export default Sidebar;
