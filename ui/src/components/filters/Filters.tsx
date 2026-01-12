import React, { useState } from 'react';
import { Card, Row, Col, Select, Input, InputNumber, Button, Space, DatePicker } from 'antd';
import { FilterOutlined, ClearOutlined, DownOutlined, UpOutlined } from '@ant-design/icons';
import { useThemeStore } from '../../stores/themeStore';
import dayjs, { Dayjs } from 'dayjs';

const { Option } = Select;
const { RangePicker } = DatePicker;

export interface FilterOption {
  key: string;
  label: string;
  type: 'select' | 'multiSelect' | 'range' | 'dateRange';
  options?: { label: string; value: string | number }[];
  value?:
    | string
    | string[]
    | [number | undefined, number | undefined]
    | [Date | undefined, Date | undefined]
    | undefined;
  placeholder?: string;
}

export interface FiltersProps {
  filters: FilterOption[];
  onFilterChange: (key: string, value: unknown) => void;
  onClearAll?: () => void;
  collapsible?: boolean;
  defaultCollapsed?: boolean;
  title?: string;
}

export const Filters: React.FC<FiltersProps> = ({
  filters,
  onFilterChange,
  onClearAll,
  collapsible = true,
  defaultCollapsed = false,
  title = 'Filters',
}) => {
  const [collapsed, setCollapsed] = useState(defaultCollapsed);
  const themeMode = useThemeStore((state) => state.mode);
  const isDark = themeMode === 'dark';

  const handleClearAll = () => {
    filters.forEach((filter) => {
      if (filter.type === 'range') {
        onFilterChange(filter.key, [undefined, undefined]);
      } else if (filter.type === 'dateRange') {
        onFilterChange(filter.key, [undefined, undefined]);
      } else {
        onFilterChange(filter.key, undefined);
      }
    });
    if (onClearAll) {
      onClearAll();
    }
  };

  const renderFilter = (filter: FilterOption) => {
    const commonProps = {
      style: { width: '100%' },
      placeholder: filter.placeholder || `Select ${filter.label}`,
    };

    switch (filter.type) {
      case 'select':
        return (
          <Select
            {...commonProps}
            value={filter.value}
            onChange={(value) => onFilterChange(filter.key, value)}
            allowClear
          >
            {filter.options?.map((option) => (
              <Option key={option.value} value={option.value}>
                {option.label}
              </Option>
            ))}
          </Select>
        );

      case 'multiSelect':
        return (
          <Select
            {...commonProps}
            mode='multiple'
            value={filter.value || []}
            onChange={(value) => onFilterChange(filter.key, value)}
            allowClear
          >
            {filter.options?.map((option) => (
              <Option key={option.value} value={option.value}>
                {option.label}
              </Option>
            ))}
          </Select>
        );

      case 'range':
        return (
          <Input.Group compact>
            <InputNumber
              style={{ width: '50%' }}
              placeholder='From'
              value={(filter.value as [number | undefined, number | undefined])?.[0]}
              onChange={(value) =>
                onFilterChange(filter.key, [
                  value,
                  (filter.value as [number | undefined, number | undefined])?.[1],
                ])
              }
              min={0}
            />
            <InputNumber
              style={{ width: '50%' }}
              placeholder='To'
              value={(filter.value as [number | undefined, number | undefined])?.[1]}
              onChange={(value) =>
                onFilterChange(filter.key, [
                  (filter.value as [number | undefined, number | undefined])?.[0],
                  value,
                ])
              }
              min={(filter.value as [number | undefined, number | undefined])?.[0] || 0}
            />
          </Input.Group>
        );

      case 'dateRange':
        return (
          <RangePicker
            style={{ width: '100%' }}
            value={
              filter.value
                ? [
                    (filter.value as [Date | undefined, Date | undefined])[0]
                      ? dayjs((filter.value as [Date | undefined, Date | undefined])[0])
                      : null,
                    (filter.value as [Date | undefined, Date | undefined])[1]
                      ? dayjs((filter.value as [Date | undefined, Date | undefined])[1])
                      : null,
                  ]
                : null
            }
            onChange={(dates: [Dayjs | null, Dayjs | null] | null) => {
              const value = dates
                ? [dates[0]?.toDate(), dates[1]?.toDate()]
                : [undefined, undefined];
              onFilterChange(filter.key, value);
            }}
          />
        );

      default:
        return null;
    }
  };

  return (
    <Card
      style={{
        background: isDark ? '#1f1f1f' : '#ffffff',
        borderRadius: '8px',
        boxShadow: isDark
          ? '0 1px 3px rgba(0,0,0,0.4)'
          : '0 1px 3px rgba(0,0,0,0.12), 0 1px 2px rgba(0,0,0,0.24)',
        marginBottom: '24px',
      }}
      title={
        <div
          style={{
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
          }}
        >
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <FilterOutlined />
            <span style={{ color: isDark ? '#fff' : '#262626' }}>{title}</span>
          </div>
          <Space>
            <Button type='text' size='small' icon={<ClearOutlined />} onClick={handleClearAll}>
              Clear All
            </Button>
            {collapsible && (
              <Button
                type='text'
                size='small'
                icon={collapsed ? <DownOutlined /> : <UpOutlined />}
                onClick={() => setCollapsed(!collapsed)}
              />
            )}
          </Space>
        </div>
      }
    >
      {!collapsed && (
        <Row gutter={[16, 16]}>
          {filters.map((filter) => (
            <Col xs={24} sm={12} md={8} lg={6} key={filter.key}>
              <div style={{ marginBottom: '8px' }}>
                <label
                  style={{
                    color: isDark ? 'rgba(255,255,255,0.65)' : 'rgba(0,0,0,0.65)',
                    fontSize: '14px',
                  }}
                >
                  {filter.label}
                </label>
              </div>
              {renderFilter(filter)}
            </Col>
          ))}
        </Row>
      )}
    </Card>
  );
};

export default Filters;
