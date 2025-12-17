import React, { useState, useEffect } from 'react';
import './NavigationMode.css'; // We'll create this

const NavigationMode = ({ route, onEndNavigation }) => {
    const [currentStepIndex, setCurrentStepIndex] = useState(0);
    const [nextStop, setNextStop] = useState(null);
    const [progress, setProgress] = useState(0);
    const [simulatedTime, setSimulatedTime] = useState(new Date());

    // Parse route data
    const summary = route?.route_summary;
    const stops = route?.charging_stops || [];

    useEffect(() => {
        if (stops.length > 0) {
            setNextStop(stops[0]);
        }
    }, [stops]);

    // Simple simulation effect
    useEffect(() => {
        const timer = setInterval(() => {
            setSimulatedTime(new Date());
            setProgress(p => {
                if (p >= 100) return 0;
                return p + 0.5;
            });
        }, 1000);
        return () => clearInterval(timer);
    }, []);

    if (!route) return null;

    return (
        <div className="navigation-mode">
            <div className="nav-header">
                <div className="nav-direction">
                    <span className="direction-arrow">⬆️</span>
                    <div className="direction-text">
                        <h3>Rotayı Takip Edin</h3>
                        <p>Hedefe {summary?.total_distance_km?.toFixed(0)} km kaldı</p>
                    </div>
                </div>
                <button className="end-nav-btn" onClick={onEndNavigation}>
                    Navigasyonu Bitir
                </button>
            </div>

            <div className="nav-map-placeholder">
                {/* In a real app, this would be the 3D map view */}
                <div className="simulated-road">
                    <div className="road-line"></div>
                    <div className="nav-car">🚗</div>
                </div>
                <div className="nav-overlay-info">
                    <div className="speed-limit">
                        <span>90</span>
                    </div>
                </div>
            </div>

            <div className="nav-footer">
                <div className="nav-stats">
                    <div className="stat-item">
                        <span className="stat-label">Varış</span>
                        <span className="stat-value">
                            {new Date(Date.now() + (summary?.total_time_hours * 3600000)).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                        </span>
                    </div>
                    <div className="stat-item">
                        <span className="stat-label">Süre</span>
                        <span className="stat-value">
                            {Math.floor(summary?.total_time_hours)}s {Math.round((summary?.total_time_hours % 1) * 60)}dk
                        </span>
                    </div>
                    <div className="stat-item">
                        <span className="stat-label">Mesafe</span>
                        <span className="stat-value">{summary?.total_distance_km?.toFixed(0)} km</span>
                    </div>
                </div>

                {nextStop && (
                    <div className="next-stop-card">
                        <div className="stop-icon">⚡</div>
                        <div className="stop-info">
                            <h4>Sonraki Şarj: {nextStop.station_name}</h4>
                            <p>{nextStop.distance_from_start?.toFixed(0)} km sonra • {nextStop.charging_power_kw}kW</p>
                        </div>
                        <div className="battery-prediction">
                            <span className="battery-level">%{nextStop.battery_on_arrival?.toFixed(0)}</span>
                            <span className="battery-label">Varışta</span>
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
};

export default NavigationMode;
