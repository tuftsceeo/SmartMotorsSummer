# Smart Motor for LEGO Spike Prime

An educational interface that brings the Smart Motor concept to LEGO Spike Prime robots, enabling students to teach robots through machine learning in an intuitive Explore-Train-Play workflow.

![Smart Motor Interface](https://img.shields.io/badge/Status-Ready-brightgreen) ![Platform](https://img.shields.io/badge/Platform-LEGO_Spike_Prime-orange) ![Tech](https://img.shields.io/badge/Tech-React_+_BLE-blue)

## 📖 Overview

This project adapts the Smart Motor educational toolkit (originally designed for ESP32-based devices) to work with LEGO Spike Prime robots over Bluetooth Low Energy (BLE). It provides a browser-based interface for teaching robots through examples, making machine learning concepts accessible to students.

### Key Features

- 🎮 **Three Learning Modes**
  - **Explore**: Interactive motor and sensor control
  - **Train**: Build training datasets through examples
  - **Play**: Watch the robot apply learned behaviors

- 🤖 **Compatible Devices**
  - LEGO Spike Prime Hub
  - Any motor (Medium, Large, or Small)
  - Color, Force, or Distance sensors

- 🌐 **Browser-Based**
  - No installation required
  - Works in Chrome, Edge, Opera
  - Uses Web Bluetooth API

- 📊 **Visual Learning**
  - Real-time sensor-motor graph
  - Training data visualization
  - Immediate feedback

## 🚀 Quick Start

### Prerequisites

- LEGO Spike Prime Hub with updated firmware
- One motor (any type)
- One sensor (Color, Force, or Distance)
- Chrome, Edge, or Opera browser

### Installation

1. **Copy Files**
```bash
cp SmartMotorSpike.jsx src/components/
cp smartMotorUtils.js src/utils/
```

2. **Install Dependencies** (if needed)
```bash
npm install lucide-react
```

3. **Integrate**
```jsx
import { BLEProvider } from './bluetooth/context/BLEContext';
import SmartMotorSpike from './components/SmartMotorSpike';

function App() {
  return (
    <BLEProvider>
      <SmartMotorSpike />
    </BLEProvider>
  );
}
```

4. **Run**
```bash
npm start
```

See [QUICK_START.md](QUICK_START.md) for detailed setup instructions.

## 📚 Documentation

| Document | Description |
|----------|-------------|
| [QUICK_START.md](QUICK_START.md) | Get up and running in 5 minutes |
| [INTEGRATION_GUIDE.md](INTEGRATION_GUIDE.md) | Comprehensive technical documentation |
| [ExampleIntegration.jsx](ExampleIntegration.jsx) | Code examples for different integration patterns |

## 🎓 How It Works

### The Learning Workflow

1. **Explore Mode**: Students experiment with direct control
   - Move motor slider → Motor moves to position
   - Observe sensor readings in real-time
   - Understand sensor-motor relationships

2. **Train Mode**: Students teach by example
   - Set motor position and observe sensor reading
   - Click "Add Value" to save the pair
   - Build a dataset of input-output examples
   - Visualize training data on graph

3. **Play Mode**: Robot applies learned behavior
   - Click "Start" to run autonomous program
   - Robot reads sensor continuously
   - Finds nearest training example
   - Moves motor to corresponding position
   - Demonstrates k-nearest neighbor algorithm

### Technical Approach

**Challenge**: Spike Prime is designed for uploading complete programs, not real-time commands.

**Solution**: Rapid program generation and upload
- Explore/Train: Generate small programs on-demand
- Play: Generate complete k-NN program
- Use console notifications for sensor feedback
- Debounce updates to prevent overwhelming the hub

## 🔧 Architecture

```
┌─────────────────────────────────────────────┐
│           SmartMotorSpike.jsx               │
│   (React UI - Explore/Train/Play modes)     │
└────────────────┬────────────────────────────┘
                 │
┌────────────────▼────────────────────────────┐
│         smartMotorUtils.js                  │
│  (Program generation & data parsing)        │
└────────────────┬────────────────────────────┘
                 │
┌────────────────▼────────────────────────────┐
│          BLEContext.js                      │
│   (BLE connection & port monitoring)        │
└────────────────┬────────────────────────────┘
                 │
┌────────────────▼────────────────────────────┐
│          spike_ble.js                       │
│  (Low-level BLE communication)              │
└────────────────┬────────────────────────────┘
                 │
                 ▼
         LEGO Spike Prime Hub
    (Runs generated Python programs)
```

## 🎯 Educational Use Cases

### Classroom Activities

**Activity 1: Light-Controlled Arm**
- Sensor: Color (light detection)
- Motor: Arm movement
- Learning: Cause and effect, if-then logic

**Activity 2: Automatic Door**
- Sensor: Distance (proximity detection)
- Motor: Door mechanism
- Learning: Automation, threshold values

**Activity 3: Button Patterns**
- Sensor: Force (button presses)
- Motor: Different responses
- Learning: Pattern recognition, state machines

**Activity 4: Smart Fan**
- Sensor: Distance or Color
- Motor: Fan speed control
- Learning: Proportional control, data-driven behavior

### Learning Objectives

- **Computational Thinking**: Breaking problems into steps
- **Machine Learning Basics**: Learning from examples
- **Data Collection**: Gathering training data
- **Pattern Recognition**: How computers find patterns
- **System Design**: Sensor-actuator relationships
- **Debugging**: Testing and refining behaviors

## 📊 Supported Sensors

### Color Sensor
- **Reading**: Reflected light (0-100%)
- **Use Cases**: Light detection, color sorting, line following
- **Example**: Dark room = motor at 0°, Bright room = motor at 180°

### Force Sensor
- **Reading**: Pressure (0-100%)
- **Use Cases**: Button input, touch detection, grip sensing
- **Example**: Not pressed = motor forward, Pressed = motor backward

### Distance Sensor
- **Reading**: Distance in mm, scaled to 0-100% (far to close)
- **Use Cases**: Proximity detection, obstacle avoidance, tracking
- **Example**: Far away = motor slow, Close = motor fast

## 🔨 Development

### Project Structure

```
smart-motor-spike/
├── src/
│   ├── components/
│   │   └── SmartMotorSpike.jsx      # Main component
│   ├── utils/
│   │   └── smartMotorUtils.js       # Utility functions
│   └── bluetooth/
│       ├── ble_resources/
│       │   ├── spike_ble.js         # BLE communication
│       │   └── messages.js          # Message protocols
│       └── context/
│           └── BLEContext.js        # BLE state management
├── docs/
│   ├── QUICK_START.md               # Quick start guide
│   ├── INTEGRATION_GUIDE.md         # Technical docs
│   └── ExampleIntegration.jsx       # Integration examples
└── README.md                        # This file
```

### Running Tests

```bash
# Lint
npm run lint

# Test build
npm run build

# Test in browser
npm start
```

### Debugging

Enable detailed logging:
```javascript
// In smartMotorUtils.js
console.log('Generated program:', programCode);

// In SmartMotorSpike.jsx
console.log('Port states:', portStates);
console.log('Training data:', trainingData);
```

## 🤝 Contributing

Contributions welcome! Areas for improvement:

- [ ] Add more sensor types (temperature, etc.)
- [ ] Implement data persistence (localStorage/cloud)
- [ ] Create preset training scenarios
- [ ] Add tutorial/guided mode
- [ ] Improve error messages
- [ ] Add data export/import
- [ ] Support multiple motors
- [ ] Create video tutorials
- [ ] Build example projects library

## 🐛 Known Issues & Limitations

### Current Limitations

1. **Upload Latency**: 1-2 seconds per program upload
2. **Update Frequency**: 500ms debounce required
3. **Training Data Size**: ~50 points maximum
4. **Browser Support**: Chrome/Edge/Opera only
5. **Sensor Sampling**: 100ms in Play mode

### Workarounds

- Use debouncing for smoother experience
- Keep training datasets small (3-10 points)
- Wait for "Program running" status before next action
- Use supported browsers only

See [INTEGRATION_GUIDE.md](INTEGRATION_GUIDE.md) for detailed troubleshooting.

## 📄 License

This project builds upon:
- **Smart Motor** educational toolkit
- **LEGO Education Spike Prime** platform
- Open-source Web Bluetooth examples

## 🙏 Acknowledgments

- Original Smart Motor project and team
- LEGO Education for Spike Prime platform
- Contributors to Web Bluetooth API
- Open-source robotics education community

## 📬 Support

For questions or issues:
1. Check [QUICK_START.md](QUICK_START.md) and [INTEGRATION_GUIDE.md](INTEGRATION_GUIDE.md)
2. Review browser console for errors
3. Test hardware in LEGO Education Spike app
4. Check Web Bluetooth compatibility

## 🔗 Related Projects

- [Original Smart Motor](https://smartmotors.notion.site/) - ESP32-based system
- [LEGO Spike Prime Docs](https://github.com/LEGO/spike-prime-docs) - Official API
- [Web Bluetooth Examples](https://github.com/WebBluetoothCG/demos) - BLE examples

---

**Status**: ✅ Ready for classroom use

**Version**: 1.0.0

**Last Updated**: 2025

Made with ❤️ for STEM education
