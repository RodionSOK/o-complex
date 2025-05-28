document.addEventListener('DOMContentLoaded', function() {
    const elements = {
        searchBtn: document.getElementById('search-btn'),
        cityInput: document.getElementById('city-input'),
        noDataMessage: document.getElementById('no-data-message'),
        weatherResults: document.getElementById('weather-results'),
        cityName: document.getElementById('city-name'),
        currentTemp: document.getElementById('current-temp'), 
        hourlyForecast: document.getElementById('hourly-forecast'),
        loadingSpinner: document.getElementById('loading-spinner')
    };
    
    if (!elements.searchBtn || !elements.cityInput || !elements.noDataMessage) {
        console.error('Critical DOM elements missing!');
        return;
    }
    
    const originalNoDataHTML = elements.noDataMessage.innerHTML;
    let isFetching = false;

    async function fetchWeather(city) {
        if (isFetching) {
            console.log('Request already in progress');
            return;
        }
        
        isFetching = true;
        showLoading(true);
        hideError();
        
        try {
            console.log('Fetching weather for:', city);
            const response = await fetch(`/api/weather/?city=${encodeURIComponent(city)}`);
            
            if (!response.ok) {
                const errorText = await response.text();
                throw new Error(`HTTP ${response.status}: ${errorText || 'Unknown error'}`);
            }
            
            const data = await response.json();
            console.log('API response:', data);
            
            if (data.error) {
                showError(data.error);
            } else {
                displayWeatherData(data);
            }
        } catch (error) {
            console.error('Fetch error:', error);
            showError(error.message || 'Unknown error');
        } finally {
            isFetching = false;
            showLoading(false);
        }
    }

    function displayWeatherData(data) {
        if (!data || !data.city || !data.hourly || !Array.isArray(data.hourly)) {
            showError('Invalid data format from server');
            return;
        }
        
        elements.noDataMessage.classList.add('d-none');
        elements.weatherResults.classList.remove('d-none');
        
        elements.cityName.textContent = data.city;
        elements.currentTemp.innerHTML = `${data.current_temp}&deg;C`;
        
        elements.hourlyForecast.innerHTML = '';
        
        data.hourly.forEach(hour => {
            try {
                const hourEl = document.createElement('div');
                hourEl.className = 'hourly-item';
                
                const timestamp = Date.parse(hour.time);
                const time = isNaN(timestamp) ? new Date() : new Date(timestamp);
                const hours = time.getHours().toString().padStart(2, '0');
                
                let trendIcon;
                switch(hour.trend) {
                    case 'up': trendIcon = '↑'; break;
                    case 'down': trendIcon = '↓'; break;
                    default: trendIcon = '→';
                }
                
                hourEl.innerHTML = `
                    <div class="hourly-time">${hours}:00</div>
                    <div class="hourly-temp">${hour.temperature}&deg;C</div>
                    <div class="hourly-trend">${trendIcon}</div>
                `;
                
                if (elements.hourlyForecast) {
                    elements.hourlyForecast.appendChild(hourEl);
                }
            } catch (e) {
                console.error('Error rendering hour:', hour, e);
            }
        });
    }

    function showError(message) {
        console.error('Showing error:', message);
        
        const errorContainer = document.createElement('div');
        errorContainer.className = 'alert alert-danger';
        errorContainer.innerHTML = `
            <p>Ошибка получения данных</p>
            <p>${message}</p>
        `;
        
        elements.noDataMessage.innerHTML = '';
        elements.noDataMessage.appendChild(errorContainer);
        elements.noDataMessage.classList.remove('d-none');
        
        if (elements.weatherResults) {
            elements.weatherResults.classList.add('d-none');
        }
    }

    function hideError() {
        elements.noDataMessage.innerHTML = originalNoDataHTML;
        elements.noDataMessage.classList.remove('d-none');
    }

    function showLoading(show) {
        if (elements.loadingSpinner) {
            elements.loadingSpinner.classList.toggle('d-none', !show);
        }
    }

    elements.searchBtn.addEventListener('click', function() {
        const city = elements.cityInput.value.trim();
        if (city) {
            fetchWeather(city);
        } else {
            showError('Пожалуйста, введите название города');
        }
    });
    
    elements.cityInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter' && !isFetching) {
            elements.searchBtn.click();
        }
    });
    
    hideError();
    showLoading(false);
});