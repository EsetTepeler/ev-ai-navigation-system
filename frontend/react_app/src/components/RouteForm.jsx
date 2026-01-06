import React, { useState, useEffect, useRef } from 'react';
import './RouteForm.css';
import { getCurrentPosition, GeolocationError } from '../utils/geolocation';
import toast from 'react-hot-toast';

const RouteForm = ({ vehicles, onPlanRoute, isPlanning, onGetCurrentLocation }) => {
  const [startAddress, setStartAddress] = useState('');
  const [endAddress, setEndAddress] = useState('');
  const [selectedVehicleId, setSelectedVehicleId] = useState('');
  const [error, setError] = useState('');
  const [vehicleSearchQuery, setVehicleSearchQuery] = useState('');
  const [showVehicleDropdown, setShowVehicleDropdown] = useState(false);

  // Address autocomplete states
  const [startSuggestions, setStartSuggestions] = useState([]);
  const [endSuggestions, setEndSuggestions] = useState([]);
  const [showStartSuggestions, setShowStartSuggestions] = useState(false);
  const [showEndSuggestions, setShowEndSuggestions] = useState(false);

  const dropdownRef = useRef(null);
  const startInputRef = useRef(null);
  const endInputRef = useRef(null);

  // Geolocation states
  const [isLoadingLocation, setIsLoadingLocation] = useState(false);
  const [userLocation, setUserLocation] = useState(null);

  // Close dropdown when clicking outside
  useEffect(() => {
    const handleClickOutside = (event) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
        setShowVehicleDropdown(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  // Geocoding function using Nominatim (OpenStreetMap)
  const geocodeAddress = async (address) => {
    try {
      // Clean and prepare address
      const cleanAddress = address.trim();

      // Add Turkey bias if not already specified
      const query = cleanAddress.includes('Türkiye') || cleanAddress.includes('Turkey')
        ? cleanAddress
        : `${cleanAddress}, Türkiye`;

      // Enhanced Nominatim search with better parameters
      const params = new URLSearchParams({
        format: 'json',
        q: query,
        limit: '10', // Get more results for better accuracy
        countrycodes: 'tr',
        addressdetails: '1', // Include detailed address breakdown
        dedupe: '0', // Don't remove duplicates (we want all options)
        'accept-language': 'tr' // Prefer Turkish results
      });

      const response = await fetch(
        `https://nominatim.openstreetmap.org/search?${params.toString()}`,
        {
          headers: {
            'User-Agent': 'EV-Navigation-App/1.0' // Good practice for Nominatim
          }
        }
      );
      const data = await response.json();

      if (data && data.length > 0) {
        console.log('Geocoding sonuçları:', data);

        // Return the best match (first result is usually most relevant)
        return {
          lat: parseFloat(data[0].lat),
          lon: parseFloat(data[0].lon),
          display_name: data[0].display_name,
          address: data[0].address // Include detailed address components
        };
      }
      return null;
    } catch (err) {
      console.error('Geocoding error:', err);
      return null;
    }
  };

  // Handle get current location
  const handleGetCurrentLocation = async () => {
    setIsLoadingLocation(true);
    const loadingToast = toast.loading('📍 Konumunuz alınıyor...');

    try {
      const position = await getCurrentPosition();
      const { lat, lon } = position;

      setUserLocation([lat, lon]);

      // Reverse geocode to get address
      try {
        const response = await fetch(
          `https://nominatim.openstreetmap.org/reverse?format=json&lat=${lat}&lon=${lon}&accept-language=tr`,
          {
            headers: {
              'User-Agent': 'EV-Navigation-App/1.0'
            }
          }
        );
        const data = await response.json();

        if (data && data.display_name) {
          setStartAddress(data.display_name);
          toast.dismiss(loadingToast);
          toast.success(' Konumunuz başlangıç adresine eklendi!', { duration: 3000 });
        } else {
          setStartAddress(`${lat.toFixed(6)}, ${lon.toFixed(6)}`);
          toast.dismiss(loadingToast);
          toast.success(' Konumunuz tespit edildi!', { duration: 3000 });
        }
      } catch (geoErr) {
        setStartAddress(`${lat.toFixed(6)}, ${lon.toFixed(6)}`);
        toast.dismiss(loadingToast);
        toast.success(' Konumunuz tespit edildi!', { duration: 3000 });
      }

      if (onGetCurrentLocation) {
        onGetCurrentLocation([lat, lon]);
      }
    } catch (err) {
      toast.dismiss(loadingToast);

      switch (err.type) {
        case GeolocationError.PERMISSION_DENIED:
          toast.error(' Konum izni reddedildi', { duration: 5000 });
          break;
        case GeolocationError.POSITION_UNAVAILABLE:
          toast.error(' Konum servisi kullanılamıyor', { duration: 4000 });
          break;
        case GeolocationError.TIMEOUT:
          toast.error(' Konum tespiti zaman aşımına uğradı', { duration: 4000 });
          break;
        default:
          toast.error('Konum alınamadı', { duration: 4000 });
      }
    } finally {
      setIsLoadingLocation(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    if (!startAddress || !endAddress) {
      setError(' Lütfen başlangıç ve varış adreslerini girin');
      return;
    }

    if (!selectedVehicleId) {
      setError(' Lütfen bir araç seçin');
      return;
    }

    // Find selected vehicle
    const vehicle = vehicles.find(v => v.id === parseInt(selectedVehicleId));
    if (!vehicle) {
      setError(' Seçilen araç bulunamadı');
      return;
    }

    // Geocode addresses
    setError(' Başlangıç adresi aranıyor...');
    const startCoords = await geocodeAddress(startAddress);
    if (!startCoords) {
      setError(` "${startAddress}" adresi bulunamadı. Örnek: "Taksim, İstanbul" veya "Ankara" şeklinde deneyin.`);
      return;
    }

    setError(' Varış adresi aranıyor...');
    const endCoords = await geocodeAddress(endAddress);
    if (!endCoords) {
      setError(` "${endAddress}" adresi bulunamadı. Örnek: "Erzurum" veya "Dadaşkent, Erzurum" şeklinde deneyin.`);
      return;
    }

    console.log(' Adresler bulundu:', {
      start: startCoords.display_name,
      end: endCoords.display_name
    });

    setError(' Rota hesaplanıyor...');

    // Call route planning
    onPlanRoute({
      start_lat: startCoords.lat,
      start_lon: startCoords.lon,
      end_lat: endCoords.lat,
      end_lon: endCoords.lon,
      vehicle_range_km: vehicle.range_km,
      battery_capacity_kwh: vehicle.battery_capacity_kwh,
      vehicle_id: vehicle.id,
      startAddress: startCoords.display_name,
      endAddress: endCoords.display_name
    });
  };

  const quickAddresses = {
    istanbul: 'İstanbul, Türkiye',
    ankara: 'Ankara, Türkiye',
    izmir: 'İzmir, Türkiye',
    antalya: 'Antalya, Türkiye',
    bursa: 'Bursa, Türkiye'
  };

  return (
    <div className="route-form-container">
      <h3> Rota Planlama</h3>

      <form onSubmit={handleSubmit} className="route-form">
        {/* Start Address */}
        <div className="form-group">
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '8px' }}>
            <label htmlFor="start-address">📍 Başlangıç Adresi</label>
            <button
              type="button"
              onClick={handleGetCurrentLocation}
              disabled={isLoadingLocation}
              style={{
                background: userLocation ? 'linear-gradient(135deg, #00ff88 0%, #00d4ff 100%)' : 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                color: 'white',
                border: 'none',
                padding: '6px 12px',
                borderRadius: '8px',
                fontSize: '12px',
                fontWeight: '600',
                cursor: isLoadingLocation ? 'wait' : 'pointer',
                opacity: isLoadingLocation ? 0.7 : 1,
                transition: 'all 0.2s ease',
                display: 'flex',
                alignItems: 'center',
                gap: '4px'
              }}
            >
              {isLoadingLocation ? '' : (userLocation ? '📍' : '🎯')}
              {isLoadingLocation ? 'Alınıyor...' : (userLocation ? 'Konum Alındı' : 'Konumumu Al')}
            </button>
          </div>
          <input
            id="start-address"
            type="text"
            value={startAddress}
            onChange={(e) => setStartAddress(e.target.value)}
            placeholder="Örn: Atatürk Caddesi, Beşiktaş, İstanbul veya Kızılay, Ankara"
            className="address-input"
          />
          <div className="quick-buttons">
            {Object.entries(quickAddresses).map(([key, value]) => (
              <button
                key={key}
                type="button"
                onClick={() => setStartAddress(value)}
                className="quick-btn"
              >
                {value.split(',')[0]}
              </button>
            ))}
          </div>
        </div>

        {/* End Address */}
        <div className="form-group">
          <label htmlFor="end-address"> Varış Adresi</label>
          <input
            id="end-address"
            type="text"
            value={endAddress}
            onChange={(e) => setEndAddress(e.target.value)}
            placeholder="Örn: Tunalı Hilmi Caddesi, Çankaya, Ankara veya Konak, İzmir"
            className="address-input"
          />
          <div className="quick-buttons">
            {Object.entries(quickAddresses).map(([key, value]) => (
              <button
                key={key}
                type="button"
                onClick={() => setEndAddress(value)}
                className="quick-btn"
              >
                {value.split(',')[0]}
              </button>
            ))}
          </div>
        </div>

        {/* Vehicle Selection with Search */}
        <div className="form-group">
          <label htmlFor="vehicle-search"> Araç Seçimi</label>
          <div className="vehicle-search-container" ref={dropdownRef}>
            <input
              id="vehicle-search"
              type="text"
              value={vehicleSearchQuery}
              onChange={(e) => {
                const newValue = e.target.value;
                setVehicleSearchQuery(newValue);
                setShowVehicleDropdown(true);
                // Clear selection when user starts typing
                if (selectedVehicleId) {
                  setSelectedVehicleId('');
                }
              }}
              onFocus={() => {
                // If a vehicle is already selected, clear everything for fresh search
                if (selectedVehicleId) {
                  setVehicleSearchQuery('');
                  setSelectedVehicleId('');
                }
                setShowVehicleDropdown(true);
              }}
              placeholder="Araç ara... (marka, model)"
              className="address-input"
            />
            {showVehicleDropdown && (
              <div className="vehicle-dropdown">
                {(() => {
                  // Levenshtein distance for fuzzy matching
                  const levenshtein = (a, b) => {
                    const matrix = [];
                    for (let i = 0; i <= b.length; i++) matrix[i] = [i];
                    for (let j = 0; j <= a.length; j++) matrix[0][j] = j;
                    for (let i = 1; i <= b.length; i++) {
                      for (let j = 1; j <= a.length; j++) {
                        if (b.charAt(i - 1) === a.charAt(j - 1)) {
                          matrix[i][j] = matrix[i - 1][j - 1];
                        } else {
                          matrix[i][j] = Math.min(
                            matrix[i - 1][j - 1] + 1,
                            matrix[i][j - 1] + 1,
                            matrix[i - 1][j] + 1
                          );
                        }
                      }
                    }
                    return matrix[b.length][a.length];
                  };

                  // Smart vehicle search
                  const searchVehicles = () => {
                    if (!vehicleSearchQuery.trim()) {
                      return vehicles.slice(0, 10);
                    }

                    const query = vehicleSearchQuery.toLowerCase().trim();
                    const scoredVehicles = vehicles.map(v => {
                      const manufacturer = (v.manufacturer || '').toLowerCase();
                      const model = (v.model || '').toLowerCase();
                      const year = (v.year || '').toString();
                      const fullName = `${manufacturer} ${model}`;

                      let score = 0;

                      // Exact match
                      if (fullName.includes(query)) {
                        score = 100;
                      } else if (manufacturer.includes(query) || model.includes(query)) {
                        score = 90;
                      } else if (year.includes(query)) {
                        score = 80;
                      } else {
                        // Multi-word search (e.g., "BMW i7")
                        const queryWords = query.split(/\s+/);
                        const nameWords = fullName.split(/\s+/);

                        let matchCount = 0;
                        queryWords.forEach(qWord => {
                          nameWords.forEach(nWord => {
                            if (nWord.includes(qWord)) {
                              matchCount += 70;
                            } else {
                              const distance = levenshtein(qWord, nWord);
                              const maxLen = Math.max(qWord.length, nWord.length);
                              if (distance <= 2 && maxLen >= 3) {
                                matchCount += Math.max(0, 60 - distance * 20);
                              }
                            }
                          });
                        });
                        score = matchCount;
                      }

                      return { vehicle: v, score };
                    });

                    return scoredVehicles
                      .filter(item => item.score > 0)
                      .sort((a, b) => b.score - a.score)
                      .slice(0, 10)
                      .map(item => item.vehicle);
                  };

                  const filteredVehicles = searchVehicles();

                  return filteredVehicles.length > 0 ? (
                    filteredVehicles.map((v) => (
                      <div
                        key={v.id}
                        className={`vehicle-dropdown-item ${selectedVehicleId === v.id.toString() ? 'selected' : ''}`}
                        onClick={() => {
                          setSelectedVehicleId(v.id.toString());
                          setVehicleSearchQuery(`${v.manufacturer} ${v.model} (${v.range_km}km)`);
                          setShowVehicleDropdown(false);
                        }}
                      >
                        <div className="vehicle-dropdown-name">
                          {v.manufacturer} {v.model} ({v.year})
                        </div>
                        <div className="vehicle-dropdown-specs">
                          {v.range_km}km | 🔋 {v.battery_capacity_kwh}kWh
                        </div>
                      </div>
                    ))
                  ) : (
                    <div className="vehicle-dropdown-empty">
                      Araç bulunamadı
                    </div>
                  );
                })()}
              </div>
            )}
          </div>
        </div>

        {/* Error Message */}
        {error && (
          <div className={`message ${error.includes('...') ? 'info' : 'error'}`}>
            {error}
          </div>
        )}

        {/* Submit Button */}
        <button
          type="submit"
          className="plan-route-btn"
          disabled={isPlanning}
        >
          {isPlanning ? 'Hesaplanıyor...' : 'Rota Hesapla'}
        </button>
      </form>

      <div className="route-info">
        <p><strong>Adres Formatları:</strong></p>
        <p> <strong>Detaylı:</strong> "Atatürk Caddesi No:15, Beşiktaş, İstanbul"</p>
        <p> <strong>Semt/İlçe:</strong> "Kadıköy, İstanbul" veya "Çankaya, Ankara"</p>
        <p> <strong>Şehir:</strong> "İstanbul", "Ankara", "İzmir"</p>
        <p style={{ fontSize: '0.85em', color: '#666' }}>
          En iyi sonuç için: Cadde/Sokak + Semt + Şehir formatını kullanın
        </p>
      </div>
    </div>
  );
};

export default RouteForm;
