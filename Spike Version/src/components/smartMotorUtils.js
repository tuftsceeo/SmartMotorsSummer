/**
 * @file smartMotorUtils.js
 * @description Utilities for Smart Motor-style real-time control with Spike Prime
 */

import { Buffer } from "buffer";

/**
 * Generate a simple motor control program for Explore/Train modes
 * This creates a minimal program that sets motor to a specific position and reads sensor
 * 
 * @param {string} motorPort - Port letter for motor (A-F)
 * @param {number} motorPosition - Target position (0-180)
 * @param {string} sensorPort - Port letter for sensor (A-F)
 * @param {string} sensorType - Type of sensor ('color', 'force', 'distance', 'none')
 * @returns {Buffer} Python code as buffer
 */
export function generateQuickControlProgram(motorPort, motorPosition, sensorPort, sensorType) {
    let code = [
        "import runloop",
        "from hub import port",
        "import motor",
    ];

    // Add sensor import based on type
    if (sensorType === 'color') {
        code.push("import color_sensor");
    } else if (sensorType === 'force') {
        code.push("import force_sensor");
    } else if (sensorType === 'distance') {
        code.push("import distance_sensor");
    }

    code.push("");
    code.push("async def main():");
    
    // Motor control
    code.push(`    motor.run_to_absolute_position(port.${motorPort}, ${motorPosition}, 1000)`);
    
    // Sensor reading
    if (sensorType === 'color') {
        code.push(`    value = color_sensor.reflection(port.${sensorPort})`);
        code.push(`    print(f"SENSOR:{value}")`);
    } else if (sensorType === 'force') {
        code.push(`    value = force_sensor.force(port.${sensorPort})`);
        code.push(`    scaled = min(100, int(value * 10))`);
        code.push(`    print(f"SENSOR:{scaled}")`);
    } else if (sensorType === 'distance') {
        code.push(`    distance = distance_sensor.distance(port.${sensorPort})`);
        code.push(`    if distance >= 0:`);
        code.push(`        value = 100 - min(100, int(distance / 2))`);
        code.push(`        print(f"SENSOR:{max(0, value)}")`);
        code.push(`    else:`);
        code.push(`        print("SENSOR:50")`);
    }
    
    code.push("");
    code.push("runloop.run(main())");

    return Buffer.from(code.join("\n"), "utf8");
}

/**
 * Generate a k-NN (k-nearest neighbor) program for Play mode
 * This creates a program that continuously reads sensor and sets motor based on training data
 * 
 * @param {string} motorPort - Port letter for motor (A-F)
 * @param {string} sensorPort - Port letter for sensor (A-F)
 * @param {string} sensorType - Type of sensor ('color', 'force', 'distance')
 * @param {Array} trainingData - Array of {sensor, motor} training points
 * @returns {Buffer} Python code as buffer
 */
export function generateKNNProgram(motorPort, sensorPort, sensorType, trainingData) {
    let code = [
        "import runloop",
        "from hub import port",
        "import motor",
        "import time",
    ];

    // Add sensor import
    if (sensorType === 'color') {
        code.push("import color_sensor");
    } else if (sensorType === 'force') {
        code.push("import force_sensor");
    } else if (sensorType === 'distance') {
        code.push("import distance_sensor");
    }

    code.push("");
    
    // Add training data as lists
    const sensorValues = trainingData.map(d => d.sensor).join(", ");
    const motorValues = trainingData.map(d => d.motor).join(", ");
    code.push(`sensor_data = [${sensorValues}]`);
    code.push(`motor_data = [${motorValues}]`);
    
    code.push("");
    code.push("def find_nearest(value):");
    code.push("    # Find nearest neighbor");
    code.push("    min_diff = float('inf')");
    code.push("    nearest_idx = 0");
    code.push("    for i, s in enumerate(sensor_data):");
    code.push("        diff = abs(value - s)");
    code.push("        if diff < min_diff:");
    code.push("            min_diff = diff");
    code.push("            nearest_idx = i");
    code.push("    return motor_data[nearest_idx]");
    
    code.push("");
    code.push("async def read_sensor():");
    
    if (sensorType === 'color') {
        code.push(`    value = color_sensor.reflection(port.${sensorPort})`);
        code.push("    return value");
    } else if (sensorType === 'force') {
        code.push(`    value = force_sensor.force(port.${sensorPort})`);
        code.push("    return min(100, int(value * 10))");
    } else if (sensorType === 'distance') {
        code.push(`    distance = distance_sensor.distance(port.${sensorPort})`);
        code.push("    if distance >= 0:");
        code.push("        value = 100 - min(100, int(distance / 2))");
        code.push("        return max(0, value)");
        code.push("    return 50");
    }
    
    code.push("");
    code.push("async def main():");
    code.push("    while True:");
    code.push("        # Read sensor");
    code.push("        sensor_value = await read_sensor()");
    code.push("        ");
    code.push("        # Find nearest neighbor");
    code.push("        target_position = find_nearest(sensor_value)");
    code.push("        ");
    code.push("        # Move motor");
    code.push(`        motor.run_to_absolute_position(port.${motorPort}, target_position, 800)`);
    code.push("        ");
    code.push("        # Output current state");
    code.push("        print(f\"SENSOR:{sensor_value} MOTOR:{target_position}\")");
    code.push("        ");
    code.push("        # Small delay");
    code.push("        await runloop.sleep_ms(100)");
    
    code.push("");
    code.push("runloop.run(main())");

    return Buffer.from(code.join("\n"), "utf8");
}

/**
 * Parse console notification for sensor data
 * Expected format: "SENSOR:50" or "SENSOR:50 MOTOR:90"
 * 
 * @param {string} message - Console message text
 * @returns {Object|null} Parsed data {sensor, motor} or null if not a valid message
 */
export function parseSensorMessage(message) {
    if (!message || typeof message !== 'string') {
        return null;
    }

    // Check for SENSOR: prefix
    if (message.includes('SENSOR:')) {
        const result = {};
        
        // Extract sensor value
        const sensorMatch = message.match(/SENSOR:(\d+)/);
        if (sensorMatch) {
            result.sensor = parseInt(sensorMatch[1], 10);
        }
        
        // Extract motor value if present
        const motorMatch = message.match(/MOTOR:(\d+)/);
        if (motorMatch) {
            result.motor = parseInt(motorMatch[1], 10);
        }
        
        return result.sensor !== undefined ? result : null;
    }
    
    return null;
}

/**
 * Debounce function to limit rapid uploads
 * 
 * @param {Function} func - Function to debounce
 * @param {number} wait - Wait time in milliseconds
 * @returns {Function} Debounced function
 */
export function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

/**
 * Map sensor type to friendly name
 */
export const SENSOR_TYPE_NAMES = {
    'none': 'No Sensor',
    'color': 'Color Sensor',
    'force': 'Force Sensor',
    'distance': 'Distance Sensor',
};

/**
 * Get sensor labels based on sensor type
 */
export function getSensorLabels(sensorType) {
    switch (sensorType) {
        case 'color':
            return { low: 'Dark', high: 'Light', icon: '💡' };
        case 'force':
            return { low: 'Released', high: 'Pressed', icon: '👆' };
        case 'distance':
            return { low: 'Far', high: 'Close', icon: '📏' };
        default:
            return { low: '', high: '', icon: '' };
    }
}

/**
 * Validate port letter
 */
export function isValidPort(port) {
    return ['A', 'B', 'C', 'D', 'E', 'F'].includes(port);
}

/**
 * Validate motor position
 */
export function isValidMotorPosition(position) {
    return typeof position === 'number' && position >= 0 && position <= 180;
}

/**
 * Validate sensor value
 */
export function isValidSensorValue(value) {
    return typeof value === 'number' && value >= 0 && value <= 100;
}
