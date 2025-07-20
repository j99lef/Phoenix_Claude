// Fix for travelers validation error
document.addEventListener('DOMContentLoaded', function() {
    console.log('Brief form fix loaded');
    
    // Override the updateTravelersField function
    window.updateTravelersField = function() {
        const travelers = [];
        const travelerItems = document.querySelectorAll('.traveler-item');
        
        travelerItems.forEach(item => {
            const nameInput = item.querySelector('input[type="text"]');
            const typeSelect = item.querySelector('select');
            
            if (nameInput && nameInput.value.trim()) {
                travelers.push(`${nameInput.value.trim()} (${typeSelect.value})`);
            }
        });
        
        const travelersField = document.getElementById('travelers_hidden');
        if (travelersField) {
            // Always ensure we have a valid value
            if (travelers.length > 0) {
                travelersField.value = travelers.join(', ');
            } else {
                // Default to current user as solo traveler
                const userName = document.querySelector('meta[name="user-name"]')?.content || 'Traveler';
                travelersField.value = `${userName} (adult)`;
            }
            console.log('Updated travelers field:', travelersField.value);
        }
    };
    
    // Auto-add current user as primary traveler
    window.initializeTravelersWithUser = function() {
        const container = document.getElementById('travelersContainer');
        if (!container) return;
        
        // Get current user info
        const userFirstName = document.querySelector('meta[name="user-first-name"]')?.content || '';
        const userLastName = document.querySelector('meta[name="user-last-name"]')?.content || '';
        const userName = (userFirstName + ' ' + userLastName).trim() || 'You';
        
        // Clear existing
        container.innerHTML = '';
        window.travelerCount = 0;
        
        // Add current user as primary
        addTravelerWithUser(userName, 'adult', true);
        
        // Update the field immediately
        updateTravelersField();
    };
    
    // Enhanced addTraveler function
    window.addTravelerWithUser = function(name, type, isPrimary) {
        window.travelerCount = (window.travelerCount || 0) + 1;
        const container = document.getElementById('travelersContainer');
        
        const travelerDiv = document.createElement('div');
        travelerDiv.className = 'traveler-item';
        travelerDiv.style.cssText = 'display: flex; gap: 10px; margin-bottom: 10px; align-items: center; padding: 10px; background: #f5f5f5; border-radius: 8px;';
        
        travelerDiv.innerHTML = `
            <input type="text" 
                   class="luxury-input" 
                   value="${name}" 
                   placeholder="Name" 
                   ${isPrimary ? 'readonly' : ''}
                   style="flex: 1; ${isPrimary ? 'background-color: #e0e0e0;' : ''}"
                   onchange="updateTravelersField()">
            <select class="luxury-select" 
                    style="width: 120px;" 
                    ${isPrimary ? 'disabled' : ''}
                    onchange="updateTravelersField()">
                <option value="adult" ${type === 'adult' ? 'selected' : ''}>Adult</option>
                <option value="child" ${type === 'child' ? 'selected' : ''}>Child</option>
                <option value="infant" ${type === 'infant' ? 'selected' : ''}>Infant</option>
                <option value="senior" ${type === 'senior' ? 'selected' : ''}>Senior</option>
            </select>
            ${isPrimary ? 
                '<span style="color: #22c55e; font-weight: 600;">You (Primary)</span>' : 
                `<button type="button" 
                         style="background: #ef4444; color: white; border: none; padding: 5px 10px; border-radius: 4px; cursor: pointer;"
                         onclick="removeTraveler(this)" 
                         title="Remove traveler">×</button>`
            }
        `;
        
        container.appendChild(travelerDiv);
        updateTravelersField();
    };
    
    // Fix form submission
    const originalSubmitBrief = window.submitBrief;
    window.submitBrief = async function(event) {
        event.preventDefault();
        
        // Ensure travelers field is updated
        updateTravelersField();
        
        // Double-check the field has a value
        const travelersField = document.getElementById('travelers_hidden');
        if (!travelersField.value || travelersField.value.trim() === '') {
            const userName = document.querySelector('meta[name="user-name"]')?.content || 'Traveler';
            travelersField.value = `${userName} (adult)`;
        }
        
        console.log('Submitting with travelers:', travelersField.value);
        
        // Call original submit function if it exists
        if (originalSubmitBrief) {
            return originalSubmitBrief(event);
        }
    };
    
    // Initialize on load
    setTimeout(() => {
        if (window.initializeTravelersWithUser) {
            initializeTravelersWithUser();
        } else if (window.initializeTravelers) {
            window.initializeTravelers();
        }
    }, 100);
});