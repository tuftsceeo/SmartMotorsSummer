/**
 * @file SmartMotorSpike.jsx
 * @description Smart Motor interface for Spike Prime - Explore, Train, and Play modes
 * Integrates with existing BLE infrastructure for real-time control
 */

import React, { useState, useRef, useEffect, useCallback } from 'react';
import { Bluetooth, Settings, HelpCircle, AlertCircle } from 'lucide-react';
import { useBLE } from '../bluetooth/context/BLEContext';
import {
    generateQuickControlProgram,
    generateKNNProgram,
    parseSensorMessage,
    debounce,
    getSensorLabels,
    isValidPort,
} from './smartMotorUtils';

const SmartMotorSpike = () => {
    // BLE Context
    const { ble, isConnected, portStates } = useBLE();

    // UI State
    const [currentPage, setCurrentPage] = useState('explore');
    const [motorValue, setMotorValue] = useState(90);
    const [sensorValue, setSensorValue] = useState(50);
    const [isPlaying, setIsPlaying] = useState(false);

    // Configuration
    const [motorPort, setMotorPort] = useState('A');
    const [sensorPort, setSensorPort] = useState('B');
    const [sensorType, setSensorType] = useState('none');

    // Training Data
    const [trainingData, setTrainingData] = useState([]);

    // Status
    const [status, setStatus] = useState('');
    const [error, setError] = useState('');

    // Canvas ref for graph
    const canvasRef = useRef(null);

    // Program slot
    const PROGRAM_SLOT = 0;

    /**
     * Upload and run a program on the Spike Prime
     */
    const uploadAndRunProgram = async (programBuffer) => {
        try {
            setStatus('Uploading program...');
            setError('');

            // Clear the slot
            await ble.sendRequest(
                new (await import('../bluetooth/ble_resources/messages')).ClearSlotRequest(PROGRAM_SLOT),
                (await import('../bluetooth/ble_resources/messages')).ClearSlotResponse
            );

            // Upload the program
            await ble.uploadProgramFile('smart.py', PROGRAM_SLOT, programBuffer);

            // Start the program
            await ble.startProgram(PROGRAM_SLOT);

            setStatus('Program running');
            return true;
        } catch (err) {
            console.error('Error uploading program:', err);
            setError(`Upload failed: ${err.message}`);
            return false;
        }
    };

    /**
     * Handle motor slider change - uploads new program with motor position
     */
    const handleMotorChange = useCallback(
        debounce(async (value) => {
            if (!isConnected || sensorType === 'none') return;

            const program = generateQuickControlProgram(
                motorPort,
                value,
                sensorPort,
                sensorType
            );

            await uploadAndRunProgram(program);
        }, 500), // Debounce 500ms to avoid too many uploads
        [isConnected, motorPort, sensorPort, sensorType]
    );

    /**
     * Handle motor slider UI change
     */
    const onMotorSliderChange = (value) => {
        setMotorValue(value);
        if (currentPage !== 'play') {
            handleMotorChange(value);
        }
    };

    /**
     * Add training value
     */
    const addTrainingValue = () => {
        if (sensorType === 'none') {
            setError('Please select a sensor type first');
            return;
        }

        const newData = {
            sensor: sensorValue,
            motor: motorValue,
        };

        setTrainingData([...trainingData, newData]);
        setStatus('Training value added');
    };

    /**
     * Delete training value
     */
    const deleteTrainingValue = (index) => {
        setTrainingData(trainingData.filter((_, i) => i !== index));
    };

    /**
     * Start/Stop Play mode
     */
    const togglePlay = async () => {
        if (!isPlaying) {
            // Start playing
            if (trainingData.length < 2) {
                setError('Need at least 2 training values to play');
                return;
            }

            if (sensorType === 'none') {
                setError('Please select a sensor type first');
                return;
            }

            // Generate k-NN program
            const program = generateKNNProgram(
                motorPort,
                sensorPort,
                sensorType,
                trainingData
            );

            const success = await uploadAndRunProgram(program);
            if (success) {
                setIsPlaying(true);
            }
        } else {
            // Stop playing
            try {
                await ble.stopProgram(PROGRAM_SLOT);
                setIsPlaying(false);
                setStatus('Stopped');
            } catch (err) {
                setError(`Stop failed: ${err.message}`);
            }
        }
    };

    /**
     * Listen for console notifications (sensor readings)
     */
    useEffect(() => {
        const handleConsoleNotification = (event) => {
            const message = event.detail?.text;
            if (!message) return;

            const parsed = parseSensorMessage(message);
            if (parsed) {
                if (parsed.sensor !== undefined) {
                    setSensorValue(parsed.sensor);
                }
                if (parsed.motor !== undefined && isPlaying) {
                    setMotorValue(parsed.motor);
                }
            }
        };

        window.addEventListener('spikeConsoleNotification', handleConsoleNotification);

        return () => {
            window.removeEventListener('spikeConsoleNotification', handleConsoleNotification);
        };
    }, [isPlaying]);

    /**
     * Draw the graph on canvas
     */
    useEffect(() => {
        if (currentPage !== 'explore' && canvasRef.current) {
            const canvas = canvasRef.current;
            const ctx = canvas.getContext('2d');

            // Clear canvas
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            // Draw sensor line (vertical)
            ctx.beginPath();
            ctx.strokeStyle = '#FFD65C';
            ctx.lineWidth = 4;
            const sensorX = (sensorValue / 100) * canvas.width;
            ctx.moveTo(sensorX, 0);
            ctx.lineTo(sensorX, canvas.height);
            ctx.stroke();

            // Draw motor line (horizontal)
            ctx.beginPath();
            ctx.strokeStyle = '#06A5FF';
            ctx.lineWidth = 4;
            const motorY = canvas.height - (motorValue / 180) * canvas.height;
            ctx.moveTo(0, motorY);
            ctx.lineTo(canvas.width, motorY);
            ctx.stroke();

            // Draw training points
            trainingData.forEach((point) => {
                ctx.beginPath();
                ctx.fillStyle = '#232323';
                ctx.arc(
                    (point.sensor / 100) * canvas.width,
                    canvas.height - (point.motor / 180) * canvas.height,
                    5,
                    0,
                    2 * Math.PI
                );
                ctx.fill();
            });
        }
    }, [currentPage, sensorValue, motorValue, trainingData]);

    /**
     * Check if ports are valid
     */
    useEffect(() => {
        if (isConnected) {
            // Check motor port
            if (motorPort && !portStates[motorPort]?.connected) {
                setError(`Motor not detected on port ${motorPort}`);
            }
            // Check sensor port
            if (sensorPort && sensorType !== 'none' && !portStates[sensorPort]?.connected) {
                setError(`Sensor not detected on port ${sensorPort}`);
            }
        }
    }, [isConnected, motorPort, sensorPort, sensorType, portStates]);

    const labels = getSensorLabels(sensorType);

    return (
        <div style={{
            fontFamily: 'Poppins, -apple-system, BlinkMacSystemFont, sans-serif',
            minHeight: '100vh',
            background: '#f5f5f5',
            paddingBottom: '2rem'
        }}>
            {/* Header */}
            <div style={{
                background: 'white',
                padding: '1rem',
                boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center'
            }}>
                <h1 style={{ margin: 0, fontSize: '1.5rem', fontWeight: 900 }}>
                    Smart Motor - Spike Prime
                </h1>
                <div style={{ display: 'flex', gap: '1rem', alignItems: 'center' }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                        <Bluetooth size={20} color={isConnected ? '#4ACB67' : '#999'} />
                        <span style={{ fontSize: '0.9rem', color: isConnected ? '#4ACB67' : '#999' }}>
                            {isConnected ? 'Connected' : 'Disconnected'}
                        </span>
                    </div>
                </div>
            </div>

            {/* Status Bar */}
            {(status || error) && (
                <div style={{
                    padding: '0.75rem',
                    background: error ? '#FEE' : '#EFE',
                    color: error ? '#C00' : '#060',
                    display: 'flex',
                    alignItems: 'center',
                    gap: '0.5rem'
                }}>
                    {error && <AlertCircle size={16} />}
                    <span>{error || status}</span>
                </div>
            )}

            {/* Port Configuration */}
            <div style={{
                background: 'white',
                padding: '1rem',
                display: 'flex',
                gap: '2rem',
                justifyContent: 'center',
                alignItems: 'center',
                boxShadow: '0 1px 3px rgba(0,0,0,0.1)'
            }}>
                <label>
                    Motor Port:
                    <select
                        value={motorPort}
                        onChange={(e) => setMotorPort(e.target.value)}
                        disabled={isPlaying}
                        style={{ marginLeft: '0.5rem', padding: '0.25rem' }}
                    >
                        {['A', 'B', 'C', 'D', 'E', 'F'].map(port => (
                            <option key={port} value={port}>{port}</option>
                        ))}
                    </select>
                </label>
                <label>
                    Sensor Port:
                    <select
                        value={sensorPort}
                        onChange={(e) => setSensorPort(e.target.value)}
                        disabled={isPlaying}
                        style={{ marginLeft: '0.5rem', padding: '0.25rem' }}
                    >
                        {['A', 'B', 'C', 'D', 'E', 'F'].map(port => (
                            <option key={port} value={port}>{port}</option>
                        ))}
                    </select>
                </label>
                <label>
                    Sensor Type:
                    <select
                        value={sensorType}
                        onChange={(e) => setSensorType(e.target.value)}
                        disabled={isPlaying}
                        style={{ marginLeft: '0.5rem', padding: '0.25rem' }}
                    >
                        <option value="none">None</option>
                        <option value="color">Color/Light</option>
                        <option value="force">Force</option>
                        <option value="distance">Distance</option>
                    </select>
                </label>
            </div>

            {/* Tabs */}
            <div style={{ display: 'flex', background: '#232323' }}>
                {[
                    { name: 'explore', label: 'Explore', color: '#06A5FF' },
                    { name: 'train', label: 'Train', color: '#C387FF' },
                    { name: 'play', label: 'Play', color: '#4ACB67' }
                ].map(tab => (
                    <button
                        key={tab.name}
                        onClick={() => {
                            if (isPlaying) {
                                setError('Stop playback before changing tabs');
                                return;
                            }
                            setCurrentPage(tab.name);
                        }}
                        style={{
                            flex: 1,
                            background: currentPage === tab.name ? tab.color : '#232323',
                            color: 'white',
                            border: 'none',
                            padding: '1.5rem',
                            fontSize: '1.5rem',
                            fontWeight: 700,
                            cursor: 'pointer',
                            transition: 'all 0.3s'
                        }}
                    >
                        {tab.label}
                    </button>
                ))}
            </div>

            {/* Explore Page */}
            {currentPage === 'explore' && (
                <ExploreView
                    motorValue={motorValue}
                    sensorValue={sensorValue}
                    sensorType={sensorType}
                    labels={labels}
                    onMotorChange={onMotorSliderChange}
                />
            )}

            {/* Train Page */}
            {currentPage === 'train' && (
                <TrainView
                    motorValue={motorValue}
                    sensorValue={sensorValue}
                    sensorType={sensorType}
                    labels={labels}
                    trainingData={trainingData}
                    canvasRef={canvasRef}
                    onMotorChange={onMotorSliderChange}
                    onAddValue={addTrainingValue}
                    onDeleteValue={deleteTrainingValue}
                />
            )}

            {/* Play Page */}
            {currentPage === 'play' && (
                <PlayView
                    motorValue={motorValue}
                    sensorValue={sensorValue}
                    labels={labels}
                    trainingData={trainingData}
                    canvasRef={canvasRef}
                    isPlaying={isPlaying}
                    onTogglePlay={togglePlay}
                />
            )}
        </div>
    );
};

// Explore View Component
const ExploreView = ({ motorValue, sensorValue, sensorType, labels, onMotorChange }) => (
    <div style={{
        padding: '2rem',
        display: 'flex',
        justifyContent: 'center',
        flexWrap: 'wrap',
        gap: '2rem'
    }}>
        {/* Motor Box */}
        <div style={{
            background: 'rgba(6, 165, 255, 0.35)',
            borderRadius: '20px',
            padding: '2rem',
            width: '300px',
            textAlign: 'center'
        }}>
            <h2 style={{ fontSize: '1.5rem', fontWeight: 700, marginBottom: '1rem' }}>Motor</h2>
            <MotorGauge value={motorValue} onChange={onMotorChange} />
        </div>

        {/* Sensor Box */}
        <div style={{
            background: 'rgba(255, 199, 0, 0.35)',
            borderRadius: '20px',
            padding: '2rem',
            width: '300px',
            textAlign: 'center'
        }}>
            <h2 style={{ fontSize: '1.5rem', fontWeight: 700, marginBottom: '1rem' }}>Sensor</h2>
            <SensorDisplay value={sensorValue} labels={labels} sensorType={sensorType} />
        </div>
    </div>
);

// Train View Component
const TrainView = ({
    motorValue,
    sensorValue,
    sensorType,
    labels,
    trainingData,
    canvasRef,
    onMotorChange,
    onAddValue,
    onDeleteValue
}) => (
    <div style={{ padding: '2rem' }}>
        <button
            onClick={onAddValue}
            style={{
                background: '#4ACB67',
                color: 'white',
                border: 'none',
                borderRadius: '20px',
                padding: '1rem 2rem',
                fontSize: '1.5rem',
                fontWeight: 700,
                cursor: 'pointer',
                display: 'block',
                margin: '0 auto 2rem'
            }}
        >
            Add Value
        </button>

        <div style={{ display: 'flex', justifyContent: 'center', gap: '2rem', flexWrap: 'wrap' }}>
            <div style={{ display: 'flex', gap: '2rem', alignItems: 'center' }}>
                <MotorGauge value={motorValue} onChange={onMotorChange} showLabel={true} />
                <canvas
                    ref={canvasRef}
                    width={400}
                    height={300}
                    style={{ border: '4px solid #232323', borderRadius: '10px' }}
                />
                <SensorDisplay value={sensorValue} labels={labels} sensorType={sensorType} vertical={true} />
            </div>

            <TrainingTable data={trainingData} onDelete={onDeleteValue} showDelete={true} />
        </div>
    </div>
);

// Play View Component
const PlayView = ({
    motorValue,
    sensorValue,
    labels,
    trainingData,
    canvasRef,
    isPlaying,
    onTogglePlay
}) => (
    <div style={{ padding: '2rem' }}>
        <button
            onClick={onTogglePlay}
            style={{
                background: isPlaying ? '#FF5151' : '#4ACB67',
                color: 'white',
                border: 'none',
                borderRadius: '20px',
                padding: '1rem 2rem',
                fontSize: '1.5rem',
                fontWeight: 700,
                cursor: 'pointer',
                display: 'block',
                margin: '0 auto 2rem'
            }}
        >
            {isPlaying ? 'Stop' : 'Start'}
        </button>

        <div style={{ display: 'flex', justifyContent: 'center', gap: '2rem', flexWrap: 'wrap' }}>
            <div style={{ display: 'flex', gap: '2rem', alignItems: 'center' }}>
                <MotorGauge value={motorValue} showLabel={true} readOnly={true} />
                <canvas
                    ref={canvasRef}
                    width={400}
                    height={300}
                    style={{ border: '4px solid #232323', borderRadius: '10px' }}
                />
                <SensorDisplay value={sensorValue} labels={labels} vertical={true} />
            </div>

            <TrainingTable data={trainingData} showDelete={false} />
        </div>
    </div>
);

// Motor Gauge Component
const MotorGauge = ({ value, onChange, showLabel, readOnly }) => (
    <div style={{ display: 'flex', alignItems: 'center', gap: '2rem', height: '300px' }}>
        <div style={{ position: 'relative', height: '100%', aspectRatio: '1/2' }}>
            <div style={{
                height: '100%',
                aspectRatio: '1/2',
                background: '#232323',
                borderTopLeftRadius: '200% 100%',
                borderBottomLeftRadius: '200% 100%',
                position: 'relative',
                overflow: 'hidden'
            }}>
                <div style={{
                    position: 'absolute',
                    left: '100%',
                    top: 0,
                    height: '100%',
                    width: '100%',
                    background: '#06A5FF',
                    transformOrigin: 'center left',
                    transform: `rotate(${value / 360}turn)`,
                    transition: 'transform 0.2s'
                }} />
            </div>
            <span style={{
                position: 'absolute',
                right: '-40px',
                top: '50%',
                transform: 'translateY(-50%)',
                fontWeight: 700,
                fontSize: '1.2rem'
            }}>{value}</span>
        </div>

        {!readOnly && (
            <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '1rem', height: '100%' }}>
                {showLabel && <p style={{ margin: 0, fontWeight: 700, writingMode: 'vertical-rl', transform: 'scale(-1)' }}>Motor</p>}
                <p style={{ margin: 0, fontWeight: 700 }}>180</p>
                <input
                    type="range"
                    min="0"
                    max="180"
                    value={value}
                    onChange={(e) => onChange(Number(e.target.value))}
                    style={{
                        writingMode: 'vertical-lr',
                        flex: 1,
                        width: '20px'
                    }}
                />
                <p style={{ margin: 0, fontWeight: 700 }}>0</p>
            </div>
        )}
    </div>
);

// Sensor Display Component
const SensorDisplay = ({ value, labels, sensorType, vertical }) => (
    <div style={vertical ? { width: '100px' } : {}}>
        {sensorType !== 'none' && (
            <>
                <div style={{ fontSize: '3rem', marginBottom: '1rem', textAlign: 'center' }}>{labels.icon}</div>
                <div style={{ display: 'flex', flexDirection: vertical ? 'column' : 'row', alignItems: 'center', gap: '0.5rem' }}>
                    <p style={{ margin: 0, fontSize: '0.9rem', fontWeight: 700 }}>{labels.low}</p>
                    <div style={{
                        flex: 1,
                        height: vertical ? '200px' : '40px',
                        width: vertical ? '40px' : '100%',
                        background: '#FFDB5E',
                        borderRadius: '10px',
                        position: 'relative',
                        overflow: 'hidden'
                    }}>
                        <div style={{
                            width: vertical ? '100%' : `${value}%`,
                            height: vertical ? `${value}%` : '100%',
                            background: '#F3BE00',
                            transition: 'all 0.2s',
                            position: vertical ? 'absolute' : 'relative',
                            bottom: vertical ? 0 : 'auto'
                        }} />
                        <span style={{
                            position: 'absolute',
                            right: vertical ? '50%' : '10px',
                            top: '50%',
                            transform: vertical ? 'translate(50%, -50%)' : 'translateY(-50%)',
                            fontWeight: 700,
                            fontSize: '0.9rem'
                        }}>{value}%</span>
                    </div>
                    <p style={{ margin: 0, fontSize: '0.9rem', fontWeight: 700 }}>{labels.high}</p>
                </div>
            </>
        )}
        {sensorType === 'none' && (
            <p style={{ color: '#999', fontStyle: 'italic' }}>No sensor selected</p>
        )}
    </div>
);

// Training Table Component
const TrainingTable = ({ data, onDelete, showDelete }) => (
    <div>
        <h2 style={{ fontSize: '1.5rem', fontWeight: 700, marginBottom: '1rem', textAlign: 'center' }}>
            Training Values
        </h2>
        {data.length === 0 ? (
            <p style={{ color: '#999', fontStyle: 'italic', textAlign: 'center' }}>No training data yet</p>
        ) : (
            <table style={{
                borderCollapse: 'collapse',
                background: 'white',
                borderRadius: '10px',
                overflow: 'hidden'
            }}>
                <thead>
                    <tr style={{ background: '#232323', color: 'white' }}>
                        <th style={{ padding: '1rem' }}>Sensor</th>
                        <th style={{ padding: '1rem' }}>Motor</th>
                        {showDelete && <th style={{ padding: '1rem' }}>Delete</th>}
                    </tr>
                </thead>
                <tbody>
                    {data.map((item, index) => (
                        <tr key={index} style={{ borderTop: '2px solid #ddd' }}>
                            <td style={{ padding: '1rem', textAlign: 'center' }}>{item.sensor}</td>
                            <td style={{ padding: '1rem', textAlign: 'center' }}>{item.motor}</td>
                            {showDelete && (
                                <td style={{ padding: '1rem', textAlign: 'center' }}>
                                    <button
                                        onClick={() => onDelete(index)}
                                        style={{
                                            background: '#FF5151',
                                            color: 'white',
                                            border: 'none',
                                            borderRadius: '50%',
                                            width: '30px',
                                            height: '30px',
                                            cursor: 'pointer',
                                            fontWeight: 'bold'
                                        }}
                                    >
                                        ×
                                    </button>
                                </td>
                            )}
                        </tr>
                    ))}
                </tbody>
            </table>
        )}
    </div>
);

export default SmartMotorSpike;
