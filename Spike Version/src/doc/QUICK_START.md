# Quick Start Guide - Smart Motor for Spike Prime

Get your Smart Motor interface running with LEGO Spike Prime in 5 minutes!

## 🚀 Quick Setup (5 Steps)

### Step 1: Copy Files

Copy these files to your React project:

```bash
# Main component
cp SmartMotorSpike.jsx src/components/

# Utilities
cp smartMotorUtils.js src/utils/

# Reference (optional)
cp spike_continuous_control.py docs/reference/
```

### Step 2: Verify Dependencies

Your project should already have these (from existing Spike Prime integration):

```json
{
  "dependencies": {
    "react": "^18.0.0",
    "lucide-react": "latest",
    "buffer": "^6.0.3"
  }
}
```

If `lucide-react` is missing:
```bash
npm install lucide-react
```

### Step 3: Add to Your App

Simplest integration - replace your App.jsx:

```jsx
import React from 'react';
import { BLEProvider } from './bluetooth/context/BLEContext';
import SmartMotorSpike from './components/SmartMotorSpike';

function App() {
  return (
    <BLEProvider>
      <SmartMotorSpike />
    </BLEProvider>
  );
}

export default App;
```

### Step 4: Run Your App

```bash
npm start
```

### Step 5: Test It!

1. **Connect**: Click Bluetooth icon, select your Spike Prime
2. **Configure**: Set Motor Port (A) and Sensor Port (B)
3. **Select Sensor**: Choose Color/Light, Force, or Distance
4. **Try Explore**: Move the motor slider
5. **Try Train**: Click "Add Value" to save training pairs
6. **Try Play**: Click "Start" to run autonomous control

## 🔌 Hardware Setup

### Required Hardware
- LEGO Spike Prime Hub
- 1 Motor (Medium, Large, or Small)
- 1 Sensor (Color, Force, or Distance)
- USB cable or Bluetooth connection

### Recommended Setup

**Example 1: Light-controlled Motor**
```
Port A: Motor
Port B: Color Sensor (for light detection)
```

**Example 2: Button-controlled Motor**
```
Port A: Motor
Port B: Force Sensor (for button presses)
```

**Example 3: Distance-controlled Motor**
```
Port A: Motor
Port B: Distance Sensor (for proximity)
```

## 🎓 First Training Session (2 minutes)

Let's create a simple light-controlled motor:

1. **Setup**
   - Connect motor to Port A
   - Connect color sensor to Port B
   - Select "Color/Light" as sensor type

2. **Explore Mode**
   - Move motor slider to 0° - note the light reading
   - Move motor slider to 180° - note the light reading
   - Switch to Train mode

3. **Train Mode**
   - Dark position: Set motor to 0°, cover sensor, click "Add Value"
   - Light position: Set motor to 180°, shine light, click "Add Value"
   - Add a middle position if desired

4. **Play Mode**
   - Click "Start"
   - Cover the sensor → motor moves to 0°
   - Shine light on sensor → motor moves to 180°
   - Magic! ✨

## 📱 Browser Requirements

- **Required**: Chrome, Edge, or Opera (Web Bluetooth support)
- **Not Supported**: Firefox, Safari
- **Mobile**: Android Chrome works, iOS Safari does not

Test Web Bluetooth support:
```javascript
if (navigator.bluetooth) {
  console.log('✅ Web Bluetooth supported');
} else {
  console.log('❌ Web Bluetooth not supported');
}
```

## 🐛 Quick Troubleshooting

### "Bluetooth icon doesn't work"
→ Check your existing BLE context is set up correctly
→ Make sure you're in a supported browser

### "Motor not detected"
→ Verify motor is plugged into the port you selected
→ Try unplugging and reconnecting
→ Check Spike Prime hub is on and charged

### "Sensor shows 50% constantly"
→ Make sure sensor type matches your physical sensor
→ Try selecting "None" then re-selecting the correct type
→ Check sensor connection

### "Upload failed"
→ Check Bluetooth connection (should show "Connected")
→ Try disconnecting and reconnecting
→ Restart the Spike Prime hub

### "Program doesn't respond to slider"
→ Wait 1-2 seconds after moving slider (debounce delay)
→ Check for error messages in red bar
→ Look at browser console for detailed errors

## 📊 Testing Checklist

Before showing to users:

- [ ] Bluetooth connects successfully
- [ ] Motor ports appear in dropdown
- [ ] Sensor ports appear in dropdown
- [ ] All three sensor types work (Color, Force, Distance)
- [ ] Explore mode: Motor responds to slider
- [ ] Explore mode: Sensor readings update
- [ ] Train mode: Can add training values
- [ ] Train mode: Can delete training values
- [ ] Train mode: Graph shows points correctly
- [ ] Play mode: Can start/stop
- [ ] Play mode: Robot responds to sensor
- [ ] Play mode: Motor position updates on screen
- [ ] Error messages display clearly
- [ ] Works in Chrome/Edge
- [ ] Mobile layout is usable (if supporting mobile)

## 🎨 Customization Ideas

### Change Colors
Edit the tab colors in SmartMotorSpike.jsx:
```javascript
{ name: 'explore', label: 'Explore', color: '#06A5FF' },  // Blue
{ name: 'train', label: 'Train', color: '#C387FF' },      // Purple  
{ name: 'play', label: 'Play', color: '#4ACB67' }         // Green
```

### Add Your Branding
Add a custom header:
```jsx
<div style={{ background: 'your-color', padding: '1rem' }}>
  <img src="your-logo.png" alt="Logo" />
  <h1>Your App Name - Smart Motor</h1>
</div>
```

### Modify Upload Speed
Change debounce time in SmartMotorSpike.jsx:
```javascript
debounce(async (value) => {
    // ... code
}, 300), // Faster: 300ms instead of 500ms
```

### Add Data Export
Add a button to export training data:
```javascript
const exportData = () => {
    const dataStr = JSON.stringify(trainingData, null, 2);
    const dataBlob = new Blob([dataStr], { type: 'application/json' });
    const url = URL.createObjectURL(dataBlob);
    const link = document.createElement('a');
    link.href = url;
    link.download = 'training-data.json';
    link.click();
};
```

## 📚 Next Steps

### Learn More
- Read `INTEGRATION_GUIDE.md` for detailed documentation
- Check `ExampleIntegration.jsx` for integration patterns
- Review `smartMotorUtils.js` for available utilities

### Extend Functionality
- Add more sensor types
- Implement data persistence (localStorage)
- Create preset training sessions
- Add export/import for training data
- Build a tutorial mode
- Add multi-motor support

### Educational Use
- Create lesson plans around the interface
- Design challenges for students
- Build example projects
- Create video tutorials

## 🤝 Getting Help

If you run into issues:

1. Check browser console for error messages
2. Verify hardware connections
3. Test in LEGO Education Spike app first
4. Review the INTEGRATION_GUIDE.md
5. Check that all files are in correct locations

## 🎉 You're Ready!

You now have a working Smart Motor interface for Spike Prime. Start experimenting and building cool projects!

### Try These Example Projects:

**1. Automatic Door**
- Train: Dark (door closed, motor 0°), Light (door open, motor 180°)
- Use: Place sensor where door should trigger

**2. Distance Follower**
- Train: Close (motor backward), Far (motor forward)
- Use: Robot maintains distance from objects

**3. Button Sequence**
- Train: Multiple press patterns with different motor positions
- Use: Create an interactive game

**4. Line Follower**
- Train: Left of line (steer right), Right of line (steer left)
- Use: Simple line-following robot

Have fun and happy building! 🤖
