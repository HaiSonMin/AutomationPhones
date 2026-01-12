import React, { useState } from 'react';
import { Card, Row, Col, Dropdown, Button } from 'antd';
import { DownOutlined, UpOutlined, BarChartOutlined } from '@ant-design/icons';
import { useThemeStore } from '../../stores/themeStore';

interface OverviewData {
  [key: string]: number;
}

interface OverviewCardProps {
  title: string;
  value: number;
  color?: string;
  icon?: React.ReactNode;
}

const OverviewCard: React.FC<OverviewCardProps> = ({ title, value, color, icon }) => {
  const themeMode = useThemeStore((state) => state.mode);
  const isDark = themeMode === 'dark';

  return (
    <Card
      style={{
        background: isDark ? '#1f1f1f' : '#ffffff',
        borderRadius: '8px',
        boxShadow: isDark
          ? '0 1px 3px rgba(0,0,0,0.4)'
          : '0 1px 3px rgba(0,0,0,0.12), 0 1px 2px rgba(0,0,0,0.24)',
      }}
      bodyStyle={{ padding: '24px' }}
    >
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
        <div>
          <p
            style={{
              margin: '0 0 8px 0',
              color: isDark ? 'rgba(255,255,255,0.65)' : 'rgba(0,0,0,0.65)',
              fontSize: '14px',
            }}
          >
            {title}
          </p>
          <p
            style={{
              margin: 0,
              color: color || (isDark ? '#fff' : '#262626'),
              fontSize: '24px',
              fontWeight: 'bold',
            }}
          >
            {value.toLocaleString()}
          </p>
        </div>
        {icon && (
          <div style={{ fontSize: '32px', color: color || (isDark ? '#1890ff' : '#1890ff') }}>
            {icon}
          </div>
        )}
      </div>
    </Card>
  );
};

export interface OverviewsProps {
  data: OverviewData;
  title?: string;
  collapsible?: boolean;
  defaultCollapsed?: boolean;
  cardConfigs?: {
    [key: string]: {
      title: string;
      color?: string;
      icon?: React.ReactNode;
    };
  };
}

export const Overviews: React.FC<OverviewsProps> = ({
  data,
  title = 'Statistics Overview',
  collapsible = true,
  defaultCollapsed = false,
  cardConfigs = {},
}) => {
  const [collapsed, setCollapsed] = useState(defaultCollapsed);
  const themeMode = useThemeStore((state) => state.mode);
  const isDark = themeMode === 'dark';

  const defaultConfigs: {
    [key: string]: { title: string; color?: string; icon?: React.ReactNode };
  } = {
    total: { title: 'Total', color: '#1890ff', icon: <BarChartOutlined /> },
    active: { title: 'Active', color: '#52c41a', icon: <BarChartOutlined /> },
    inactive: { title: 'Inactive', color: '#ff4d4f', icon: <BarChartOutlined /> },
    pending: { title: 'Pending', color: '#faad14', icon: <BarChartOutlined /> },
    online: { title: 'Online', color: '#52c41a', icon: <BarChartOutlined /> },
    offline: { title: 'Offline', color: '#ff4d4f', icon: <BarChartOutlined /> },
    connected: { title: 'Connected', color: '#1890ff', icon: <BarChartOutlined /> },
    disconnected: { title: 'Disconnected', color: '#ff4d4f', icon: <BarChartOutlined /> },
  };

  const configs = { ...defaultConfigs, ...cardConfigs };

  const dropdownItems = [
    {
      key: 'toggle',
      label: (
        <Button
          type='text'
          icon={collapsed ? <DownOutlined /> : <UpOutlined />}
          onClick={() => setCollapsed(!collapsed)}
        >
          {collapsed ? 'Expand' : 'Collapse'}
        </Button>
      ),
    },
  ];

  return (
    <div style={{ marginBottom: '24px' }}>
      <div
        style={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          marginBottom: '16px',
        }}
      >
        <h3
          style={{
            margin: 0,
            color: isDark ? '#fff' : '#262626',
            fontSize: '18px',
            fontWeight: '500',
          }}
        >
          {title}
        </h3>
        {collapsible && (
          <Dropdown menu={{ items: dropdownItems }} trigger={['click']}>
            <Button type='text' icon={collapsed ? <DownOutlined /> : <UpOutlined />} />
          </Dropdown>
        )}
      </div>

      {!collapsed && (
        <Row gutter={[16, 16]}>
          {Object.entries(data).map(([key, value]) => {
            const config = configs[key] || { title: key };
            return (
              <Col xs={24} sm={12} md={8} lg={6} key={key}>
                <OverviewCard
                  title={config.title}
                  value={value}
                  color={config.color}
                  icon={config.icon}
                />
              </Col>
            );
          })}
        </Row>
      )}
    </div>
  );
};

export default Overviews;
