/**
 * Common JavaScript functionality for TravelAiGent
 */

// User Profile Dropdown
function toggleProfileDropdown(event) {
    event.stopPropagation();
    const dropdown = document.getElementById('profileDropdown');
    if (dropdown) {
        dropdown.classList.toggle('show');
    }
}

// Close dropdown when clicking outside
document.addEventListener('click', function(event) {
    const dropdown = document.getElementById('profileDropdown');
    const trigger = document.querySelector('.luxury-profile-trigger');
    
    if (dropdown && trigger && !trigger.contains(event.target) && !dropdown.contains(event.target)) {
        dropdown.classList.remove('show');
    }
});

// Initialize dropdown styles if not present
document.addEventListener('DOMContentLoaded', function() {
    // Add dropdown styles if not already present
    if (!document.querySelector('style[data-dropdown-styles]')) {
        const style = document.createElement('style');
        style.setAttribute('data-dropdown-styles', 'true');
        style.textContent = `
            .luxury-profile {
                position: relative;
            }
            
            .luxury-profile-trigger {
                display: flex;
                align-items: center;
                gap: var(--space-luxury-sm);
                cursor: pointer;
                padding: var(--space-luxury-sm) var(--space-luxury-md);
                border-radius: 12px;
                transition: var(--transition-luxury);
            }
            
            .luxury-profile-trigger:hover {
                background: rgba(255, 255, 255, 0.1);
            }
            
            .luxury-dropdown-menu {
                position: absolute;
                top: calc(100% + 10px);
                right: 0;
                background: var(--luxury-white);
                border: 1px solid var(--luxury-stone);
                border-radius: 12px;
                box-shadow: var(--shadow-luxury-elevated);
                min-width: 220px;
                opacity: 0;
                visibility: hidden;
                transform: translateY(-10px);
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
                z-index: 9999;
            }
            
            .luxury-dropdown-menu.show {
                opacity: 1;
                visibility: visible;
                transform: translateY(0);
            }
            
            .luxury-dropdown-item {
                display: flex;
                align-items: center;
                gap: var(--space-luxury-md);
                padding: var(--space-luxury-md) var(--space-luxury-lg);
                color: var(--luxury-obsidian);
                text-decoration: none;
                transition: var(--transition-luxury);
                font-size: 0.95rem;
            }
            
            .luxury-dropdown-item:first-child {
                border-radius: 12px 12px 0 0;
            }
            
            .luxury-dropdown-item:last-child {
                border-radius: 0 0 12px 12px;
            }
            
            .luxury-dropdown-item:hover {
                background: var(--luxury-pearl);
                color: var(--luxury-gold);
            }
            
            .luxury-dropdown-item i {
                width: 20px;
                text-align: center;
                color: var(--luxury-gold);
            }
            
            .luxury-dropdown-divider {
                height: 1px;
                background: var(--luxury-stone);
                margin: var(--space-luxury-xs) 0;
            }
        `;
        document.head.appendChild(style);
    }
});