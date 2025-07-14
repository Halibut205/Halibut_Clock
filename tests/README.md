# Tests Directory

This directory contains test files for the Timer application.

## Test Files

### Core Functionality Tests
- **`test_daily_stats.py`** - Tests for daily statistics tracking and management
- **`test_monthly_stats.py`** - Tests for monthly statistics aggregation and analysis

### UI and Chart Tests  
- **`test_enhanced_ui.py`** - Tests for enhanced user interface components
- **`test_enhanced_charts.py`** - Tests for matplotlib chart generation with separated sessions/tasks
- **`test_charts.py`** - Basic chart functionality tests
- **`test_features.py`** - Tests for advanced features and integrations

### Demo and Visual Tests
- **`visual_demo.py`** - Visual demonstration of UI components and features

## Running Tests

To run individual tests:
```bash
python tests/test_daily_stats.py
python tests/test_enhanced_charts.py
```

## Test Coverage

The tests cover:
- ✅ Daily statistics tracking and calculation
- ✅ Chart generation and matplotlib integration  
- ✅ Separated sessions and tasks visualization
- ✅ Enhanced UI components and styling
- ✅ Monthly statistics aggregation
- ✅ Visual components and user experience

## Requirements

Tests require:
- `matplotlib>=3.5.0` for chart testing
- `tkinter` for UI testing (usually included with Python)
- All main application dependencies

## Notes

- Charts are tested with both separated tabs (sessions/tasks) and combined views
- UI tests include enhanced styling and professional appearance
- All efficiency chart transparency issues have been resolved

## Running Demos

Demo files can be run directly:

```bash
python tests/demo_stats_window.py
```

**Note**: Some demos may require the main application to be running or specific data files to be present.
