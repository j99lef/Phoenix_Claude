// Fix for travelers validation error
document.addEventListener('DOMContentLoaded', function() {
    console.log('Brief form fix loaded');
    
    // Store original functions
    const originalAddTraveler = window.addTraveler;
    const originalInitializeTravelers = window.initializeTravelers;
    
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
    
    // Enhanced addTraveler function that allows adding more travelers
    window.addTraveler = function() {
        window.travelerCount = (window.travelerCount || 0) + 1;
        const container = document.getElementById('travelersContainer');
        
        const travelerDiv = document.createElement('div');
        travelerDiv.className = 'traveler-item';
        travelerDiv.style.display = 'flex';
        travelerDiv.style.gap = 'var(--space-luxury-md)';
        travelerDiv.style.alignItems = 'center';
        travelerDiv.style.marginBottom = 'var(--space-luxury-md)';
        
        travelerDiv.innerHTML = `
            <input type="text" class="luxury-input" placeholder="Traveler name" style="flex: 1;" 
                   onchange="updateTravelersField()" data-traveler-id="${window.travelerCount}">
            <select class="luxury-select" style="min-width: 120px;" onchange="updateTravelersField()" data-traveler-id="${window.travelerCount}">
                <option value="adult">Adult</option>
                <option value="child">Child</option>
                <option value="senior">Senior</option>
                <option value="infant">Infant</option>
            </select>
            <button type="button" class="luxury-button luxury-button-danger" onclick="removeTraveler(this)" style="padding: var(--space-luxury-sm);">
                <i class="fas fa-trash"></i>
            </button>
        `;
        
        container.appendChild(travelerDiv);
        updateTravelersField();
    };
    
    // Override initializeTravelers to add user as primary
    window.initializeTravelers = function() {
        const existingTravelers = document.querySelector('meta[name="existing-travelers"]')?.content || '';
        const container = document.getElementById('travelersContainer');
        
        // Get current user info
        const userFirstName = document.querySelector('meta[name="user-first-name"]')?.content || '';
        const userLastName = document.querySelector('meta[name="user-last-name"]')?.content || '';
        const userName = (userFirstName + ' ' + userLastName).trim() || 'You';
        
        if (existingTravelers && existingTravelers.trim() && existingTravelers !== '2 Adults') {
            // Parse existing travelers
            originalInitializeTravelers.call(this);
        } else {
            // Add user as primary traveler
            window.travelerCount = 1;
            
            const travelerDiv = document.createElement('div');
            travelerDiv.className = 'traveler-item';
            travelerDiv.style.display = 'flex';
            travelerDiv.style.gap = 'var(--space-luxury-md)';
            travelerDiv.style.alignItems = 'center';
            travelerDiv.style.marginBottom = 'var(--space-luxury-md)';
            
            travelerDiv.innerHTML = `
                <input type="text" class="luxury-input" value="${userName}" placeholder="Traveler name" style="flex: 1; background-color: #e0e0e0;" 
                       readonly onchange="updateTravelersField()" data-traveler-id="1">
                <select class="luxury-select" style="min-width: 120px;" disabled onchange="updateTravelersField()" data-traveler-id="1">
                    <option value="adult" selected>Adult</option>
                    <option value="child">Child</option>
                    <option value="senior">Senior</option>
                    <option value="infant">Infant</option>
                </select>
                <span style="color: #22c55e; font-weight: 600; min-width: 100px;">You (Primary)</span>
            `;
            
            container.appendChild(travelerDiv);
            updateTravelersField();
        }
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
        if (window.initializeTravelers) {
            window.initializeTravelers();
        }
    }, 100);
});