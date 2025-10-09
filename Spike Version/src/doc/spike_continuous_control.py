"""
Smart Motor Real-Time Control Program
This program runs continuously on the Spike Prime hub to enable
real-time sensor reading and motor control for Explore/Train modes.

The program:
- Continuously reads sensor values from a specified port
- Outputs sensor readings via console notifications
- Listens for motor position commands
- Can be controlled via the hub buttons for emergency stop
"""

import runloop
import time
from hub import port, button, light_matrix
import motor
import color_sensor
import force_sensor
import distance_sensor

# Configuration - These will be set by the web app
MOTOR_PORT = port.A  # Default motor port
SENSOR_PORT = port.B  # Default sensor port
SENSOR_TYPE = "none"  # Options: "color", "force", "distance", "light", "none"

# Global state
current_motor_position = 90
target_motor_position = 90
is_running = True

async def read_sensor():
    """Read the current sensor value and return 0-100 scale"""
    global SENSOR_PORT, SENSOR_TYPE
    
    try:
        if SENSOR_TYPE == "color":
            # Read color sensor - use reflected light (0-100)
            value = color_sensor.reflection(SENSOR_PORT)
            return value
        elif SENSOR_TYPE == "force":
            # Read force sensor - return force percentage (0-100)
            value = force_sensor.force(SENSOR_PORT)
            # Force sensor returns 0-10 Newtons, scale to 0-100
            return min(100, int(value * 10))
        elif SENSOR_TYPE == "distance":
            # Read distance sensor - return distance as percentage
            # Distance sensor returns mm, we'll scale 0-200mm to 0-100%
            distance = distance_sensor.distance(SENSOR_PORT)
            if distance < 0:
                return 0
            # Invert so close = high value
            value = 100 - min(100, int(distance / 2))
            return max(0, value)
        else:
            # No sensor or unknown type
            return 50
    except:
        return 50

async def control_motor():
    """Control motor to match target position"""
    global MOTOR_PORT, current_motor_position, target_motor_position
    
    try:
        # Get current position
        current = motor.absolute_position(MOTOR_PORT)
        if current is None:
            current = 90
            
        # Calculate difference
        diff = target_motor_position - current
        
        # If difference is significant, move motor
        if abs(diff) > 5:
            # Run motor at speed proportional to difference
            speed = max(-1000, min(1000, diff * 10))
            motor.run(MOTOR_PORT, speed)
            current_motor_position = current
        else:
            # Close enough, stop motor
            motor.stop(MOTOR_PORT)
            current_motor_position = target_motor_position
            
    except:
        # Motor not connected or error
        pass

async def send_sensor_data():
    """Send sensor value via console notification"""
    sensor_value = await read_sensor()
    # Format: S:<sensor_value>:M:<motor_position>
    print(f"SM:{sensor_value}:{current_motor_position}")

async def check_for_commands():
    """Check for incoming commands from serial/console
    Commands expected format: CMD:M:<position>
    """
    global target_motor_position, is_running
    
    # Note: In actual implementation, we'd need to read from serial input
    # For now, this is a placeholder. The web app will send motor commands
    # via uploading new programs or using a different mechanism
    pass

async def emergency_stop():
    """Check for emergency stop via hub button"""
    global is_running
    
    if button.pressed(button.LEFT) and button.pressed(button.RIGHT):
        is_running = False
        motor.stop(MOTOR_PORT)
        light_matrix.write("X")
        return True
    return False

async def main():
    """Main control loop"""
    global is_running
    
    # Show ready indicator
    light_matrix.write("S")
    
    # Main loop - runs continuously
    loop_count = 0
    while is_running:
        # Check for emergency stop
        if await emergency_stop():
            break
        
        # Control motor to target position
        await control_motor()
        
        # Send sensor data every 5 loops (~100ms)
        if loop_count % 5 == 0:
            await send_sensor_data()
        
        # Check for new commands
        await check_for_commands()
        
        # Small delay to prevent overwhelming the system
        await runloop.sleep_ms(20)
        
        loop_count += 1
    
    # Cleanup
    motor.stop(MOTOR_PORT)
    light_matrix.write("E")

# Run the main loop
runloop.run(main())
