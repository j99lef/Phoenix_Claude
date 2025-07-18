// Travel AiGent Frontend JavaScript

let refreshInterval;
let lastUpdateTime = 0;

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    console.log('Travel AiGent Dashboard Initializing...');
    
    // Load initial data
    refreshData();
    
    // Set up auto-refresh every 30 seconds
    refreshInterval = setInterval(refreshData, 30000);
    
    // Initialize Bootstrap toasts
    initializeToasts();
    
    // Add real-time status updates
    initializeRealTimeUpdates();
});

// Real-time update system
function initializeRealTimeUpdates() {
    // Update status indicator with live connection status
    setInterval(updateConnectionStatus, 5000);
    
    // Add visual feedback for data freshness
    addDataFreshnessIndicators();
}

function updateConnectionStatus() {
    const indicator = document.getElementById('status-indicator');
    if (!indicator) return;
    
    // Check if we can reach the API
    fetch('/api/status', { method: 'HEAD' })
        .then(response => {
            if (response.ok) {
                updateStatusIndicator('success', 'System Active');
                updateLastUpdateTime();
            } else {
                updateStatusIndicator('warning', 'System Issues');
            }
        })
        .catch(() => {
            updateStatusIndicator('error', 'Connection Lost');
        });
}

function addDataFreshnessIndicators() {
    // Add timestamps to show when data was last updated
    const timestamp = new Date().toLocaleTimeString();
    const statusElements = ['last-check', 'active-briefs', 'total-deals', 'notifications-sent'];
    
    statusElements.forEach(id => {
        const element = document.getElementById(id);
        if (element && element.parentElement) {
            let timeIndicator = element.parentElement.querySelector('.last-updated');
            if (!timeIndicator) {
                timeIndicator = document.createElement('small');
                timeIndicator.className = 'last-updated text-muted';
                timeIndicator.style.fontSize = '10px';
                timeIndicator.style.display = 'block';
                element.parentElement.appendChild(timeIndicator);
            }
            timeIndicator.textContent = `Updated: ${timestamp}`;
        }
    });
}

function updateLastUpdateTime() {
    const timeElements = document.querySelectorAll('.last-updated');
    const timestamp = new Date().toLocaleTimeString();
    timeElements.forEach(el => {
        el.textContent = `Updated: ${timestamp}`;
    });
}

// Refresh all data from the API
async function refreshData() {
    try {
        const currentTime = Date.now();
        
        // Prevent too frequent updates
        if (currentTime - lastUpdateTime < 5000) {
            return;
        }
        
        lastUpdateTime = currentTime;
        
        // Show loading states
        showLoadingState();
        
        // Load status, briefs, and deals in parallel
        await Promise.all([
            loadStatus(),
            loadBriefs(),
            loadDeals()
        ]);
        
        updateStatusIndicator('success', 'System Active');
        hideLoadingState();
        
    } catch (error) {
        console.error('Error refreshing data:', error);
        updateStatusIndicator('error', 'Connection Error');
        hideLoadingState();
        handleApiError(error, 'refreshing dashboard data');
    }
}

// Show loading states across the dashboard
function showLoadingState() {
    // Add loading class to main elements
    const elementsToLoad = [
        'last-check',
        'active-briefs', 
        'total-deals',
        'notifications-sent',
        'packages-container'
    ];
    
    elementsToLoad.forEach(id => {
        const element = document.getElementById(id);
        if (element) {
            if (id === 'packages-container') {
                element.innerHTML = `
                    <div class="col-12 text-center py-5">
                        <div class="spinner-border text-primary" role="status">
                            <span class="visually-hidden">Loading...</span>
                        </div>
                        <p class="mt-3 text-muted">Loading travel packages...</p>
                    </div>
                `;
            } else {
                element.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';
            }
        }
    });
}

// Hide loading states
function hideLoadingState() {
    // Loading states will be replaced by actual data in load functions
}

// Load system status
async function loadStatus() {
    try {
        const response = await fetch('/api/status');
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }
        
        const status = await response.json();
        
        // Update status cards
        updateElement('last-check', formatLastCheck(status.last_check));
        updateElement('active-briefs', status.active_briefs || 0);
        
        // Update deals found with dynamic coloring
        const totalDeals = status.total_deals_found || 0;
        const dealsElement = document.getElementById('total-deals');
        if (dealsElement) {
            dealsElement.textContent = totalDeals;
            if (totalDeals > 0) {
                dealsElement.classList.add('success');
            } else {
                dealsElement.classList.remove('success');
            }
        }
        
        // Update notifications sent with dynamic coloring
        const notificationsSent = status.notifications_sent || 0;
        const notificationsElement = document.getElementById('notifications-sent');
        if (notificationsElement) {
            notificationsElement.textContent = notificationsSent;
            if (notificationsSent > 0) {
                notificationsElement.classList.add('success');
            } else {
                notificationsElement.classList.remove('success');
            }
        }
        
        // Make Active Briefs stat card clickable if we have briefs
        const activeBriefsCard = document.querySelector('.stat-card:nth-child(2)');
        if (activeBriefsCard && (status.active_briefs || 0) > 0) {
            activeBriefsCard.classList.add('clickable');
            activeBriefsCard.style.cursor = 'pointer';
            activeBriefsCard.style.transition = 'all 0.2s ease';
            activeBriefsCard.title = 'Click to view all active briefs';
            activeBriefsCard.onclick = () => {
                // Show list of all active briefs
                showActiveBriefsList();
            };
            activeBriefsCard.onmouseover = () => {
                activeBriefsCard.style.transform = 'translateY(-2px)';
                activeBriefsCard.style.boxShadow = '0 4px 20px rgba(0,0,0,0.15)';
            };
            activeBriefsCard.onmouseout = () => {
                activeBriefsCard.style.transform = 'translateY(0)';
                activeBriefsCard.style.boxShadow = '0 2px 10px rgba(0,0,0,0.1)';
            };
        }
        
    } catch (error) {
        console.error('Error loading status:', error);
        console.error('Status error details:', error.message, error.stack);
        throw error;
    }
}

// Load active travel briefs
async function loadBriefs() {
    try {
        const response = await fetch('/api/briefs');
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }
        
        const briefs = await response.json();
        
        // Store briefs globally for modal access
        window.currentBriefs = briefs;
        
        renderBriefs(briefs);
        
    } catch (error) {
        console.error('Error loading briefs:', error);
        renderBriefsError(error.message);
    }
}

// Load qualified travel packages (AI score 8+ only)
async function loadDeals(filters = {}) {
    try {
        // Build query parameters
        const params = new URLSearchParams();
        if (filters.min_score) params.append('min_score', filters.min_score);
        if (filters.max_price) params.append('max_price', filters.max_price);
        if (filters.destination) params.append('destination', filters.destination);
        if (filters.limit) params.append('limit', filters.limit);
        
        const url = `/api/deals${params.toString() ? '?' + params.toString() : ''}`;
        const response = await fetch(url);
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }
        
        const deals = await response.json();
        
        // Store deals globally for detailed view access
        window.currentDeals = deals;
        
        renderTravelPackages(deals);
        
    } catch (error) {
        console.error('Error loading qualified packages:', error);
        handleApiError(error, 'loading travel packages');
        renderTravelPackagesEmpty('Unable to load travel packages');
    }
}

// Render travel briefs
function renderBriefs(briefs) {
    const container = document.getElementById('briefs-container');
    
    if (!briefs || briefs.length === 0) {
        container.innerHTML = `
            <div class="empty-state">
                <i class="fas fa-clipboard-list"></i>
                <h5>No Active Travel Briefs</h5>
                <p>No travel briefs are currently active. Add some in your Google Sheet to start monitoring deals.</p>
            </div>
        `;
        return;
    }
    
    const briefsHtml = briefs.map(brief => `
        <div class="brief-card card fade-in-up" onclick="viewBriefDetail('${brief.Brief_ID || brief.brief_id || 'TB-OCT-2025'}')" style="cursor: pointer;">
            <div class="card-body">
                <div class="row">
                    <div class="col-md-8">
                        <h6 class="brief-destinations">${escapeHtml(brief.Destinations || 'No destinations')}</h6>
                        <p class="brief-dates mb-2">
                            <i class="fas fa-calendar me-1"></i>
                            ${escapeHtml(brief.Travel_Dates || 'No dates specified')}
                        </p>
                        <p class="brief-budget mb-2">
                            <i class="fas fa-pound-sign me-1"></i>
                            Budget: £${escapeHtml(brief.Budget_Max || 'No limit')}
                        </p>
                        <small class="text-muted">
                            <i class="fas fa-users me-1"></i>
                            ${escapeHtml(brief.Travelers || '4 people')}
                        </small>
                    </div>
                    <div class="col-md-4 text-end">
                        <span class="badge bg-primary">${escapeHtml(brief.Brief_ID || 'No ID')}</span>
                        <br><small class="text-muted mt-2 d-block">
                            ${escapeHtml(brief.Trip_Duration || 'Duration not specified')}
                        </small>
                    </div>
                </div>
                ${brief.AI_Instructions ? `
                    <div class="mt-2">
                        <small class="text-info">
                            <i class="fas fa-robot me-1"></i>
                            ${escapeHtml(brief.AI_Instructions)}
                        </small>
                    </div>
                ` : ''}
            </div>
        </div>
    `).join('');
    
    container.innerHTML = briefsHtml;
}

// Render briefs error
function renderBriefsError(message) {
    const container = document.getElementById('briefs-container');
    container.innerHTML = `
        <div class="alert alert-warning">
            <i class="fas fa-exclamation-triangle me-2"></i>
            Failed to load travel briefs: ${escapeHtml(message)}
        </div>
    `;
}

// Render recent deals
function renderDeals(deals) {
    const container = document.getElementById('deals-container');
    
    if (!deals || deals.length === 0) {
        container.innerHTML = `
            <div class="empty-state">
                <i class="fas fa-plane"></i>
                <h5>No Deals Found Yet</h5>
                <p>The system hasn't found any travel deals yet. Check back after the next scheduled search.</p>
            </div>
        `;
        return;
    }
    
    const dealsHtml = deals.map(deal => {
        const score = parseInt(deal.AI_Score || deal.score || 0);
        const scoreClass = score >= 8 ? 'high' : score >= 6 ? 'medium' : 'low';
        const recommendation = deal.Recommendation || deal.recommendation || 'IGNORE';
        const recommendationClass = recommendation.toLowerCase().replace('_', '-');
        
        return `
            <div class="deal-card card fade-in-up">
                <div class="card-body">
                    <div class="row align-items-center">
                        <div class="col-md-2">
                            <div class="deal-score ${scoreClass}">
                                ${score}/10
                            </div>
                            <small class="text-muted">AI Score</small>
                        </div>
                        <div class="col-md-3">
                            <div class="deal-route">
                                ${escapeHtml(deal.Origin || deal.origin || 'N/A')} → 
                                ${escapeHtml(deal.Destination || deal.destination || 'N/A')}
                            </div>
                            <small class="text-muted">
                                ${escapeHtml(deal.Departure_Date || deal.departure_date || 'No date')}
                            </small>
                        </div>
                        <div class="col-md-2">
                            <div class="deal-price">
                                £${parseFloat(deal.Total_Price || deal.total_price || 0).toLocaleString()}
                            </div>
                            <small class="text-muted">Total price</small>
                        </div>
                        <div class="col-md-2">
                            <span class="deal-airline">
                                ${escapeHtml(deal.Airline || deal.airline || 'N/A')}
                            </span>
                        </div>
                        <div class="col-md-2">
                            <span class="badge recommendation-badge recommendation-${recommendationClass}">
                                ${recommendation}
                            </span>
                        </div>
                        <div class="col-md-1 text-end">
                            <small class="text-muted">
                                ${formatTimestamp(deal.Timestamp || deal.found_at)}
                            </small>
                        </div>
                    </div>
                    ${deal.Action_Summary || deal.action_summary ? `
                        <div class="row mt-2">
                            <div class="col-12">
                                <small class="text-info">
                                    <i class="fas fa-lightbulb me-1"></i>
                                    ${escapeHtml(deal.Action_Summary || deal.action_summary)}
                                </small>
                            </div>
                        </div>
                    ` : ''}
                </div>
            </div>
        `;
    }).join('');
    
    container.innerHTML = dealsHtml;
}

// Render deals error
function renderDealsError(message) {
    const container = document.getElementById('deals-container');
    container.innerHTML = `
        <div class="alert alert-warning">
            <i class="fas fa-exclamation-triangle me-2"></i>
            Failed to load recent deals: ${escapeHtml(message)}
        </div>
    `;
}

// Run manual search
async function runManualSearch() {
    const button = event.target;
    const originalText = button.innerHTML;
    
    button.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Searching...';
    button.disabled = true;
    
    try {
        const response = await fetch('/api/run-search', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }
        
        const result = await response.json();
        showToast('success', 'Manual search started successfully!');
        
        // Refresh data after a short delay
        setTimeout(refreshData, 3000);
        
    } catch (error) {
        console.error('Error running manual search:', error);
        showToast('error', 'Failed to start manual search: ' + error.message);
    } finally {
        button.innerHTML = originalText;
        button.disabled = false;
    }
}

// Test notification
async function testNotification() {
    const button = event.target;
    const originalText = button.innerHTML;
    
    button.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Sending...';
    button.disabled = true;
    
    try {
        const response = await fetch('/api/test-notification', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }
        
        const result = await response.json();
        showToast('success', 'Test notification sent successfully!');
        
    } catch (error) {
        console.error('Error sending test notification:', error);
        showToast('error', 'Failed to send test notification: ' + error.message);
    } finally {
        button.innerHTML = originalText;
        button.disabled = false;
    }
}

// Utility functions
function updateElement(id, value) {
    const element = document.getElementById(id);
    if (element) {
        element.textContent = value;
    }
}

function updateStatusIndicator(type, message) {
    const indicator = document.getElementById('status-indicator');
    const icon = indicator.querySelector('i');
    
    // Reset classes
    icon.classList.remove('text-success', 'text-danger', 'text-warning');
    
    // Set new status
    switch (type) {
        case 'success':
            icon.classList.add('text-success');
            break;
        case 'error':
            icon.classList.add('text-danger');
            break;
        case 'warning':
            icon.classList.add('text-warning');
            break;
    }
    
    indicator.childNodes[1].textContent = message;
}

function formatLastCheck(timestamp) {
    if (!timestamp || timestamp === 'Never') {
        return 'Never';
    }
    
    try {
        const date = new Date(timestamp);
        const now = new Date();
        const diffMinutes = Math.floor((now - date) / (1000 * 60));
        
        if (diffMinutes < 1) {
            return 'Just now';
        } else if (diffMinutes < 60) {
            return `${diffMinutes}m ago`;
        } else if (diffMinutes < 1440) {
            return `${Math.floor(diffMinutes / 60)}h ago`;
        } else {
            return date.toLocaleDateString();
        }
    } catch (error) {
        return timestamp;
    }
}

function formatTimestamp(timestamp) {
    if (!timestamp) return 'Unknown';
    
    try {
        const date = new Date(timestamp);
        return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    } catch (error) {
        return 'Invalid';
    }
}

function escapeHtml(text) {
    if (!text) return '';
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function initializeToasts() {
    // Initialize Bootstrap toast components
    const toastElements = document.querySelectorAll('.toast');
    toastElements.forEach(toastEl => {
        new bootstrap.Toast(toastEl);
    });
}

function showToast(type, message) {
    const toastId = type === 'error' ? 'errorToast' : 'successToast';
    const bodyId = type === 'error' ? 'errorToastBody' : 'successToastBody';
    
    // Enhance error messages with helpful context
    if (type === 'error') {
        message = enhanceErrorMessage(message);
    }
    
    document.getElementById(bodyId).textContent = message;
    
    const toast = new bootstrap.Toast(document.getElementById(toastId));
    toast.show();
}

function enhanceErrorMessage(message) {
    // Common error patterns and user-friendly alternatives
    const errorMappings = {
        'HTTP 404': 'Resource not found. Please try refreshing the page.',
        'HTTP 500': 'Server error. Please try again in a few minutes.',
        'HTTP 503': 'Service temporarily unavailable. Please try again later.',
        'Network request failed': 'Connection problem. Please check your internet connection.',
        'Failed to fetch': 'Unable to connect to server. Please check your connection.',
        'timeout': 'Request timed out. Please try again.',
        'CORS': 'Security restriction. Please contact support if this persists.'
    };
    
    // Check for known error patterns
    for (const [pattern, friendlyMessage] of Object.entries(errorMappings)) {
        if (message.toLowerCase().includes(pattern.toLowerCase())) {
            return friendlyMessage;
        }
    }
    
    // Return original message if no mapping found
    return message;
}

function handleApiError(error, context = '') {
    console.error(`API Error ${context}:`, error);
    
    let userMessage = 'An unexpected error occurred.';
    
    if (error.message) {
        userMessage = enhanceErrorMessage(error.message);
    }
    
    if (context) {
        userMessage += ` (${context})`;
    }
    
    showToast('error', userMessage);
    
    // Update connection status if this seems like a connectivity issue
    if (error.message && (error.message.includes('fetch') || error.message.includes('network'))) {
        updateStatusIndicator('error', 'Connection Issues');
    }
}

// Handle page visibility changes to pause/resume updates
document.addEventListener('visibilitychange', function() {
    if (document.hidden) {
        // Page is hidden, clear interval
        if (refreshInterval) {
            clearInterval(refreshInterval);
        }
    } else {
        // Page is visible, restart interval
        refreshData();
        refreshInterval = setInterval(refreshData, 30000);
    }
});

// Handle window focus/blur for real-time updates
window.addEventListener('focus', function() {
    // Refresh data when window gains focus
    refreshData();
});

// Premium Travel Package Rendering Functions
function renderTravelPackages(deals) {
    const container = document.getElementById('packages-container');
    if (!container) return;
    
    // Check if there are any deals that meet criteria
    if (!deals || deals.length === 0) {
        renderTravelPackagesEmpty('No travel packages meet your criteria yet');
        return;
    }
    
    // Create curated package cards from qualified deals
    const packagesHtml = deals.map((deal, index) => {
        const destination = deal.Destination || deal.destination || 'Unknown';
        const price = parseFloat(deal.Total_Price || deal.total_price || 0);
        const score = parseFloat(deal.AI_Score || deal.ai_score || 0);
        const departureDate = deal.Departure_Date || deal.departure_date || '';
        const returnDate = deal.Return_Date || deal.return_date || '';
        
        // Determine destination theme for styling
        const destClass = getDestinationClass(destination);
        const destIcon = getDestinationIcon(destination);
        const scoreClass = score >= 9 ? 'excellent' : score >= 8.5 ? 'good' : 'fair';
        const scoreLabel = score >= 9 ? 'Excellent' : score >= 8.5 ? 'Great Value' : 'Good Option';
        
        // Calculate duration
        const duration = getDuration(departureDate, returnDate);
        
        return `
            <div class="package-card" onclick="showPackageDetails('${deal.id || index}')">
                <div class="package-image ${destClass}">
                    <div class="destination-icon">${destIcon}</div>
                    <div class="package-badge">AI Score: ${score.toFixed(1)}</div>
                </div>
                <div class="package-content">
                    <div class="package-destination">${escapeHtml(destination)} Experience</div>
                    <div class="package-subtitle">October Half Term • ${duration}</div>
                    <div class="package-details">
                        <div class="package-detail">
                            <i class="fas fa-plane"></i>
                            <span>From London</span>
                        </div>
                        <div class="package-detail">
                            <i class="fas fa-hotel"></i>
                            <span>${deal.hotel_name || deal.Hotel_Name || 'Quality Hotels'}</span>
                        </div>
                        <div class="package-detail">
                            <i class="fas fa-star"></i>
                            <span>${deal.hotel_rating || deal.Hotel_Rating || '4+'} Star Hotel</span>
                        </div>
                        <div class="package-detail">
                            <i class="fas fa-users"></i>
                            <span>Family of 4</span>
                        </div>
                    </div>
                    <div class="package-price">
                        <div>
                            <div class="package-price-amount">£${price.toLocaleString()}</div>
                            <div class="package-price-per">total for family</div>
                        </div>
                        <div class="package-score ${scoreClass}">
                            <i class="fas fa-star"></i>
                            <span>${scoreLabel}</span>
                        </div>
                    </div>
                </div>
            </div>
        `;
    }).join('');
    
    // Replace static packages with real curated ones
    container.innerHTML = packagesHtml;
}

function renderTravelPackagesEmpty(message) {
    const container = document.getElementById('packages-container');
    if (!container) return;
    
    container.innerHTML = `
        <div class="col-12">
            <div class="empty-state-premium">
                <div class="empty-icon">🏖️</div>
                <h3>Discovering Your Perfect Trip</h3>
                <p>Our AI is continuously monitoring travel deals that match your family's preferences. 
                   We only show packages that score 8+ and meet all your criteria.</p>
                <div class="empty-stats">
                    <div class="empty-stat">
                        <div class="stat-number">24/7</div>
                        <div class="stat-label">Monitoring</div>
                    </div>
                    <div class="empty-stat">
                        <div class="stat-number">8+</div>
                        <div class="stat-label">AI Score Required</div>
                    </div>
                    <div class="empty-stat">
                        <div class="stat-number">16</div>
                        <div class="stat-label">Destinations Tracked</div>
                    </div>
                </div>
                <button class="btn btn-primary" onclick="runManualSearch()">
                    <i class="fas fa-search me-2"></i>Search Now
                </button>
            </div>
        </div>
    `;
}

// Helper functions for package rendering
function getDestinationClass(destination) {
    const dest = destination.toLowerCase();
    if (dest.includes('barcelona') || dest.includes('bar')) return 'dest-barcelona';
    if (dest.includes('rome') || dest.includes('italy')) return 'dest-rome';
    if (dest.includes('valencia') || dest.includes('val')) return 'dest-valencia';
    if (dest.includes('greece') || dest.includes('crete') || dest.includes('athens')) return 'dest-greece';
    if (dest.includes('portugal') || dest.includes('lisbon')) return 'dest-portugal';
    if (dest.includes('cyprus') || dest.includes('malta')) return 'dest-cyprus';
    return 'dest-barcelona'; // Default
}

function getDestinationIcon(destination) {
    const dest = destination.toLowerCase();
    if (dest.includes('barcelona') || dest.includes('spain')) return '🏖️';
    if (dest.includes('rome') || dest.includes('italy')) return '🏛️';
    if (dest.includes('greece') || dest.includes('crete')) return '🏛️';
    if (dest.includes('portugal')) return '🌊';
    if (dest.includes('cyprus') || dest.includes('malta')) return '🌊';
    return '✈️'; // Default
}

function getDuration(departureDate, returnDate) {
    if (!departureDate || !returnDate) return '5-7 nights';
    
    try {
        const departure = new Date(departureDate);
        const returnD = new Date(returnDate);
        const diffTime = Math.abs(returnD - departure);
        const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
        return `${diffDays} nights`;
    } catch {
        return '5-7 nights';
    }
}

function showPackageDetails(packageId) {
    // Show detailed package information including accommodation
    const deals = window.currentDeals || [];
    const deal = deals.find(d => (d.id || d.Deal_ID) === packageId) || deals[parseInt(packageId)];
    
    if (!deal) {
        showToast('error', 'Package details not available. Please refresh the page.');
        return;
    }
    
    // Store deal data globally for booking functions
    window.currentDealData = deal;
    
    // Extract deal information
    const destination = deal.Destination || deal.destination || 'Unknown';
    const price = parseFloat(deal.Total_Price || deal.total_price || 0);
    const flightPrice = parseFloat(deal.Flight_Price || deal.flight_price || 0);
    const hotelPrice = parseFloat(deal.Hotel_Price || deal.hotel_price || 0);
    const hotelName = deal.hotel_name || deal.Hotel_Name || 'Premium 4+ Star Hotel';
    const hotelRating = deal.hotel_rating || deal.Hotel_Rating || '4+';
    const aiScore = parseFloat(deal.AI_Score || deal.ai_score || 0);
    const departureDate = deal.Departure_Date || deal.departure_date || '';
    const returnDate = deal.Return_Date || deal.return_date || '';
    const roomType = deal.room_type || deal.Room_Type || 'Family Room';
    const aiAnalysis = deal.ai_analysis || deal.AI_Analysis || 'Quality family package with excellent value proposition';
    
    // Populate modal fields
    document.getElementById('modal-destination').textContent = `${destination} Experience`;
    document.getElementById('modal-package-title').textContent = `${destination} Family Package`;
    document.getElementById('modal-package-subtitle').textContent = `Travel Package • ${getDuration(departureDate, returnDate)}`;
    document.getElementById('modal-ai-score').innerHTML = `<i class="fas fa-robot me-1"></i>AI Score: ${aiScore.toFixed(1)}/10`;
    
    // Flight details
    document.getElementById('modal-departure-date').textContent = departureDate || 'TBA';
    document.getElementById('modal-return-date').textContent = returnDate || 'TBA';
    document.getElementById('modal-departure-airport').textContent = 'London Airports (LHR/LGW/STN)';
    document.getElementById('modal-airline').textContent = 'Premium Airlines';
    document.getElementById('modal-flight-duration').textContent = '2-4 hours';
    document.getElementById('modal-flight-price').textContent = `£${flightPrice.toLocaleString()}`;
    
    // Hotel details
    document.getElementById('modal-hotel-name').textContent = hotelName;
    document.getElementById('modal-hotel-rating').innerHTML = generateStarRating(hotelRating);
    document.getElementById('modal-room-type').textContent = roomType;
    document.getElementById('modal-checkin').textContent = departureDate || 'TBA';
    document.getElementById('modal-checkout').textContent = returnDate || 'TBA';
    document.getElementById('modal-hotel-price').textContent = `£${hotelPrice.toLocaleString()}`;
    
    // Amenities
    const amenities = deal.hotel_amenities || ['Pool', 'WiFi', 'Family Friendly', 'Restaurant'];
    document.getElementById('modal-amenities').innerHTML = amenities.map(amenity => 
        `<span class="amenity-tag">${amenity}</span>`
    ).join('');
    
    // AI Analysis
    document.getElementById('modal-ai-analysis').innerHTML = `
        <p class="analysis-text">${aiAnalysis}</p>
        <div class="row mt-3">
            <div class="col-md-6">
                <h6 class="text-success">Key Highlights:</h6>
                <ul class="analysis-list">
                    <li>${hotelRating}+ star accommodation</li>
                    <li>Family-friendly facilities</li>
                    <li>Premium location in ${destination}</li>
                    <li>Excellent value for money</li>
                </ul>
            </div>
            <div class="col-md-6">
                <h6 class="text-warning">Considerations:</h6>
                <ul class="analysis-list">
                    <li>Popular travel dates</li>
                    <li>Book early for best rates</li>
                </ul>
            </div>
        </div>
    `;
    
    // Package totals
    document.getElementById('modal-total-price').textContent = `£${price.toLocaleString()}`;
    const savings = Math.round(price * 0.05); // Estimate 5% package savings
    document.getElementById('modal-savings').innerHTML = `<i class="fas fa-tag me-1"></i>Save £${savings} vs booking separately`;
    
    // Show the modal
    const modal = new bootstrap.Modal(document.getElementById('packageDetailsModal'));
    modal.show();
}

function generateStarRating(rating) {
    const numStars = parseInt(rating) || 4;
    const stars = Array(5).fill().map((_, i) => 
        i < numStars ? '<i class="fas fa-star text-warning"></i>' : '<i class="far fa-star text-muted"></i>'
    ).join('');
    return `${stars}<span class="ms-2">${rating}+ Star</span>`;
}

function showActiveBriefsList() {
    // Show modal with list of all active briefs
    const briefs = window.currentBriefs || [];
    
    if (!briefs || briefs.length === 0) {
        showToast('info', 'No active briefs found. Please refresh the page.');
        return;
    }
    
    // Create briefs list HTML
    const briefsListHtml = briefs.map(brief => {
        const briefId = brief.Brief_ID || brief.brief_id || 'Unknown';
        const briefName = brief.Brief_Name || brief.brief_name || 'Unnamed Brief';
        const destinations = brief.Destinations || brief.destinations || 'No destinations';
        const travelDates = brief.Travel_Dates || brief.travel_dates || 'No dates';
        const budget = brief.Budget_Max || brief.budget_max || 'No budget';
        const priority = brief.Priority || brief.priority || 'Medium';
        
        const priorityClass = priority.toLowerCase() === 'high' ? 'text-danger' : 
                             priority.toLowerCase() === 'medium' ? 'text-warning' : 'text-success';
        
        return `
            <div class="brief-list-item" onclick="viewBriefDetail('${briefId}')" style="cursor: pointer;">
                <div class="row">
                    <div class="col-md-8">
                        <h6 class="brief-id-name">
                            <span class="badge bg-primary me-2">${briefId}</span>
                            ${briefName}
                        </h6>
                        <p class="brief-destinations mb-1">
                            <i class="fas fa-map-marker-alt me-1"></i>
                            ${destinations}
                        </p>
                        <p class="brief-dates mb-1">
                            <i class="fas fa-calendar me-1"></i>
                            ${travelDates}
                        </p>
                        <p class="brief-budget mb-0">
                            <i class="fas fa-pound-sign me-1"></i>
                            Budget: £${budget}
                        </p>
                    </div>
                    <div class="col-md-4 text-end">
                        <span class="priority-badge ${priorityClass}">
                            <i class="fas fa-flag me-1"></i>
                            ${priority} Priority
                        </span>
                        <div class="mt-2">
                            <small class="text-muted">Click to view details</small>
                        </div>
                    </div>
                </div>
            </div>
        `;
    }).join('');
    
    // Create modal HTML
    const modalHtml = `
        <div class="modal fade" id="activeBriefsModal" tabindex="-1">
            <div class="modal-dialog modal-lg">
                <div class="modal-content">
                    <div class="modal-header bg-primary text-white">
                        <h5 class="modal-title">
                            <i class="fas fa-clipboard-list me-2"></i>
                            Active Travel Briefs (${briefs.length})
                        </h5>
                        <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        <div class="briefs-list">
                            ${briefsListHtml}
                        </div>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                        <button type="button" class="btn btn-primary" onclick="runManualSearch()">
                            <i class="fas fa-search me-2"></i>Search All Briefs
                        </button>
                    </div>
                </div>
            </div>
        </div>
        
        <style>
        .brief-list-item {
            background: #f8f9fa;
            border: 1px solid #e9ecef;
            border-radius: 8px;
            padding: 16px;
            margin-bottom: 12px;
            transition: all 0.2s ease;
        }
        
        .brief-list-item:hover {
            background: #e3f2fd;
            border-color: #2196f3;
            transform: translateY(-1px);
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        
        .brief-id-name {
            color: #2c3e50;
            margin-bottom: 8px;
            font-weight: 600;
        }
        
        .brief-destinations {
            color: #495057;
            font-size: 0.9rem;
        }
        
        .brief-dates, .brief-budget {
            color: #6c757d;
            font-size: 0.85rem;
        }
        
        .priority-badge {
            font-size: 0.8rem;
            font-weight: 600;
            padding: 4px 8px;
            border-radius: 12px;
            background: rgba(255,255,255,0.1);
        }
        </style>
    `;
    
    // Remove existing modal and add new one
    const existingModal = document.getElementById('activeBriefsModal');
    if (existingModal) {
        existingModal.remove();
    }
    
    document.body.insertAdjacentHTML('beforeend', modalHtml);
    
    // Show the modal
    const modal = new bootstrap.Modal(document.getElementById('activeBriefsModal'));
    modal.show();
}

function copyDealDetails() {
    const dealData = window.currentDealData || {};
    
    const destination = dealData.Destination || dealData.destination || 'Destination';
    const departureDate = dealData.Departure_Date || dealData.departure_date || 'TBA';
    const returnDate = dealData.Return_Date || dealData.return_date || 'TBA';
    const flightPrice = dealData.Flight_Price || dealData.flight_price || 'TBA';
    const hotelName = dealData.Hotel_Name || dealData.hotel_name || 'Quality Hotel';
    const hotelRating = dealData.Hotel_Rating || dealData.hotel_rating || '4+';
    const roomType = dealData.Room_Type || dealData.room_type || 'Family Room';
    const hotelPrice = dealData.Hotel_Price || dealData.hotel_price || 'TBA';
    const totalPrice = dealData.Total_Price || dealData.total_price || dealData.price || 'TBA';
    const aiScore = dealData.AI_Score || dealData.ai_score || 'N/A';
    
    const dealText = `
🏖️ TRAVEL DEAL FOUND - ${destination}

✈️ FLIGHT DETAILS:
• From: London (LHR/LGW/STN)
• To: ${destination}
• Departure: ${departureDate}
• Return: ${returnDate}
• Price: £${flightPrice}

🏨 HOTEL DETAILS:
• Hotel: ${hotelName}
• Rating: ${hotelRating}★
• Room: ${roomType}
• Check-in: ${departureDate}
• Check-out: ${returnDate}
• Price: £${hotelPrice}

💰 TOTAL PACKAGE: £${totalPrice}
🤖 AI SCORE: ${aiScore}/10

Found by Lefley TravelAiGent
    `.trim();
    
    navigator.clipboard.writeText(dealText).then(() => {
        showToast('success', 'Deal details copied to clipboard!');
    }).catch(() => {
        showToast('error', 'Failed to copy details. Please try again.');
    });
}

function bookFlightDirect() {
    const dealData = window.currentDealData || {};
    const destination = dealData.Destination || dealData.destination || 'Barcelona';
    const departureDate = dealData.Departure_Date || dealData.departure_date || '';
    const returnDate = dealData.Return_Date || dealData.return_date || '';
    
    // Build search parameters for major booking sites
    const searchParams = new URLSearchParams({
        origin: 'LON', // London (all airports)
        destination: getAirportCode(destination),
        departure: formatDateForBooking(departureDate),
        return: formatDateForBooking(returnDate),
        adults: '2',
        children: '2',
        cabin: 'economy'
    });
    
    // Create booking options modal
    const bookingOptions = [
        {
            name: 'Skyscanner',
            url: `https://www.skyscanner.com/transport/flights/lon/${getAirportCode(destination)}/${formatDateForBooking(departureDate)}/${formatDateForBooking(returnDate)}/?adults=2&children=2&adultsv2=2&childrenv2=2%7C8%7C12&cabinclass=economy`,
            logo: '✈️'
        },
        {
            name: 'Google Flights',
            url: `https://www.google.com/travel/flights/search?tfs=CBwQAhokagwIAxIIL20vMDRqcGwSCjIwMjUtMTA`,
            logo: '🔍'
        },
        {
            name: 'Expedia',
            url: `https://www.expedia.co.uk/Flights-Search?trip=roundtrip&leg1=from%3ALondon%2Cto%3A${destination}%2Cdeparture%3A${formatDateForBooking(departureDate)}TANYT&leg2=from%3A${destination}%2Cto%3ALondon%2Cdeparture%3A${formatDateForBooking(returnDate)}TANYT&passengers=adults%3A2%2Cchildren%3A2%2Cseniors%3A0%2Cinfants%3A0&options=cabinclass%3Aeconomy`,
            logo: '🌍'
        },
        {
            name: 'British Airways',
            url: `https://www.britishairways.com/travel/book/public/en_gb`,
            logo: '🇬🇧'
        }
    ];
    
    showBookingModal('flight', bookingOptions, dealData);
}

function bookHotelDirect() {
    const dealData = window.currentDealData || {};
    const destination = dealData.Destination || dealData.destination || 'Barcelona';
    const checkIn = dealData.Departure_Date || dealData.departure_date || '';
    const checkOut = dealData.Return_Date || dealData.return_date || '';
    const hotelName = dealData.Hotel_Name || dealData.hotel_name || '';
    
    // Create hotel booking options
    const bookingOptions = [
        {
            name: 'Booking.com',
            url: `https://www.booking.com/searchresults.html?ss=${encodeURIComponent(destination + ' ' + hotelName)}&checkin=${formatDateForBooking(checkIn)}&checkout=${formatDateForBooking(checkOut)}&group_adults=2&group_children=2&no_rooms=1`,
            logo: '🏨'
        },
        {
            name: 'Hotels.com',
            url: `https://www.hotels.com/search.do?destination=${encodeURIComponent(destination)}&q-check-in=${formatDateForBooking(checkIn)}&q-check-out=${formatDateForBooking(checkOut)}&q-rooms=1&q-room-0-adults=2&q-room-0-children=2`,
            logo: '🏩'
        },
        {
            name: 'Expedia Hotels',
            url: `https://www.expedia.co.uk/Hotels-Search?destination=${encodeURIComponent(destination)}&startDate=${formatDateForBooking(checkIn)}&endDate=${formatDateForBooking(checkOut)}&rooms=1&adults=2&children=2`,
            logo: '🌟'
        },
        {
            name: 'Airbnb',
            url: `https://www.airbnb.co.uk/search?location=${encodeURIComponent(destination)}&checkin=${formatDateForBooking(checkIn)}&checkout=${formatDateForBooking(checkOut)}&adults=2&children=2`,
            logo: '🏠'
        }
    ];
    
    showBookingModal('hotel', bookingOptions, dealData);
}

function showBookingModal(type, options, dealData) {
    const modalTitle = type === 'flight' ? 'Book Your Flight' : 'Book Your Hotel';
    const icon = type === 'flight' ? 'fa-plane' : 'fa-hotel';
    
    const optionsHtml = options.map(option => `
        <div class="booking-option" onclick="openBookingLink('${option.url}')">
            <div class="booking-logo">${option.logo}</div>
            <div class="booking-info">
                <h6>${option.name}</h6>
                <p class="text-muted">Compare ${type} prices and book directly</p>
            </div>
            <div class="booking-arrow">
                <i class="fas fa-external-link-alt"></i>
            </div>
        </div>
    `).join('');
    
    const modalHtml = `
        <div class="modal fade" id="bookingModal" tabindex="-1">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header bg-primary text-white">
                        <h5 class="modal-title">
                            <i class="fas ${icon} me-2"></i>${modalTitle}
                        </h5>
                        <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        <div class="alert alert-info">
                            <i class="fas fa-info-circle me-2"></i>
                            Choose your preferred booking platform. You'll be redirected to complete your booking with pre-filled search details.
                        </div>
                        <div class="booking-options">
                            ${optionsHtml}
                        </div>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                    </div>
                </div>
            </div>
        </div>
        
        <style>
        .booking-option {
            display: flex;
            align-items: center;
            padding: 16px;
            border: 1px solid #e0e0e0;
            border-radius: 8px;
            margin-bottom: 12px;
            cursor: pointer;
            transition: all 0.2s ease;
        }
        
        .booking-option:hover {
            border-color: #2196f3;
            background: #f8f9ff;
            transform: translateY(-1px);
        }
        
        .booking-logo {
            font-size: 24px;
            margin-right: 16px;
            width: 40px;
            text-align: center;
        }
        
        .booking-info {
            flex: 1;
        }
        
        .booking-info h6 {
            margin: 0;
            color: #2c3e50;
        }
        
        .booking-info p {
            margin: 0;
            font-size: 0.85rem;
        }
        
        .booking-arrow {
            color: #6c757d;
        }
        </style>
    `;
    
    // Remove existing modal
    const existingModal = document.getElementById('bookingModal');
    if (existingModal) {
        existingModal.remove();
    }
    
    document.body.insertAdjacentHTML('beforeend', modalHtml);
    
    const modal = new bootstrap.Modal(document.getElementById('bookingModal'));
    modal.show();
}

function openBookingLink(url) {
    window.open(url, '_blank');
    showToast('info', 'Opening booking site in new tab...');
    
    // Close the booking modal
    const modal = bootstrap.Modal.getInstance(document.getElementById('bookingModal'));
    if (modal) {
        modal.hide();
    }
}

function getAirportCode(destination) {
    const codes = {
        'Barcelona': 'BCN',
        'Rome': 'FCO',
        'Valencia': 'VLC',
        'Naples': 'NAP',
        'Athens': 'ATH',
        'Lisbon': 'LIS',
        'Porto': 'OPO',
        'Dubai': 'DXB',
        'Bangkok': 'BKK',
        'Cancun': 'CUN',
        'Miami': 'MIA',
        'San Jose': 'SJO'
    };
    return codes[destination] || destination.slice(0, 3).toUpperCase();
}

function formatDateForBooking(dateStr) {
    if (!dateStr) return '';
    try {
        const date = new Date(dateStr);
        return date.toISOString().split('T')[0]; // YYYY-MM-DD format
    } catch {
        return '';
    }
}

function viewBriefDetail(briefId) {
    // Navigate to the brief detail page
    window.location.href = `/brief/${briefId}`;
}

// Filter management functions
function toggleFilters() {
    const panel = document.getElementById('filterPanel');
    const isVisible = panel.style.display !== 'none';
    
    if (isVisible) {
        panel.style.display = 'none';
    } else {
        panel.style.display = 'block';
        // Add animation
        panel.style.opacity = '0';
        setTimeout(() => {
            panel.style.opacity = '1';
            panel.style.transition = 'opacity 0.3s ease';
        }, 10);
    }
}

function applyFilters() {
    const filters = {
        min_score: document.getElementById('minScoreFilter').value,
        max_price: document.getElementById('maxPriceFilter').value,
        destination: document.getElementById('destinationFilter').value.trim(),
        limit: document.getElementById('limitFilter').value
    };
    
    // Show loading state
    const container = document.getElementById('packages-container');
    container.innerHTML = `
        <div class="col-12 text-center py-5">
            <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">Loading...</span>
            </div>
            <p class="mt-3 text-muted">Filtering travel packages...</p>
        </div>
    `;
    
    // Load deals with filters
    loadDeals(filters);
    
    showToast('info', 'Filters applied successfully!');
}

function clearFilters() {
    // Reset all filter values to defaults
    document.getElementById('minScoreFilter').value = '8';
    document.getElementById('maxPriceFilter').value = '3000';
    document.getElementById('destinationFilter').value = '';
    document.getElementById('limitFilter').value = '10';
    
    // Apply cleared filters
    applyFilters();
    
    showToast('info', 'Filters cleared!');
}

console.log('Travel AiGent Dashboard JavaScript Loaded');
