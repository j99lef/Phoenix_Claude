/**
 * School Holiday Intelligence for Family Groups
 * Automatically suggests school holiday dates based on UK school terms
 */

// UK School Holiday dates for 2025 (approximate)
const UK_SCHOOL_HOLIDAYS_2025 = {
    // Spring Term
    'february-half-term': {
        start: '2025-02-17',
        end: '2025-02-21',
        name: 'February Half Term',
        type: 'half-term'
    },
    'easter-holidays': {
        start: '2025-04-14',
        end: '2025-04-25',
        name: 'Easter Holidays',
        type: 'main-holiday'
    },
    
    // Summer Term
    'may-half-term': {
        start: '2025-05-26',
        end: '2025-05-30',
        name: 'May Half Term',
        type: 'half-term'
    },
    'summer-holidays': {
        start: '2025-07-21',
        end: '2025-09-01',
        name: 'Summer Holidays',
        type: 'main-holiday'
    },
    
    // Autumn Term
    'october-half-term': {
        start: '2025-10-27',
        end: '2025-10-31',
        name: 'October Half Term',
        type: 'half-term'
    },
    'christmas-holidays': {
        start: '2025-12-22',
        end: '2026-01-05',
        name: 'Christmas Holidays',
        type: 'main-holiday'
    }
};

// Council/Local Authority variations (example for some major areas)
const COUNCIL_VARIATIONS = {
    'london': {
        'february-half-term': { start: '2025-02-17', end: '2025-02-21' },
        'easter-holidays': { start: '2025-04-14', end: '2025-04-28' },
        'may-half-term': { start: '2025-05-26', end: '2025-05-30' },
        'summer-holidays': { start: '2025-07-21', end: '2025-09-01' },
        'october-half-term': { start: '2025-10-27', end: '2025-10-31' },
        'christmas-holidays': { start: '2025-12-22', end: '2026-01-05' }
    },
    'birmingham': {
        'february-half-term': { start: '2025-02-17', end: '2025-02-21' },
        'easter-holidays': { start: '2025-04-14', end: '2025-04-25' },
        'may-half-term': { start: '2025-05-26', end: '2025-05-30' },
        'summer-holidays': { start: '2025-07-21', end: '2025-09-01' },
        'october-half-term': { start: '2025-10-27', end: '2025-10-31' },
        'christmas-holidays': { start: '2025-12-22', end: '2026-01-05' }
    },
    'manchester': {
        'february-half-term': { start: '2025-02-17', end: '2025-02-21' },
        'easter-holidays': { start: '2025-04-14', end: '2025-04-25' },
        'may-half-term': { start: '2025-05-26', end: '2025-05-30' },
        'summer-holidays': { start: '2025-07-21', end: '2025-09-01' },
        'october-half-term': { start: '2025-10-27', end: '2025-10-31' },
        'christmas-holidays': { start: '2025-12-22', end: '2026-01-05' }
    }
};

/**
 * Get school holidays for a specific council/borough
 * @param {string} council - Council name (e.g., 'london', 'birmingham')
 * @returns {Object} School holiday dates
 */
function getSchoolHolidays(council = null) {
    if (council && COUNCIL_VARIATIONS[council.toLowerCase()]) {
        return COUNCIL_VARIATIONS[council.toLowerCase()];
    }
    return UK_SCHOOL_HOLIDAYS_2025;
}

/**
 * Get next upcoming school holiday
 * @param {string} council - Council name
 * @returns {Object} Next holiday information
 */
function getNextSchoolHoliday(council = null) {
    const holidays = getSchoolHolidays(council);
    const today = new Date();
    
    let nextHoliday = null;
    let minDiff = Infinity;
    
    Object.entries(holidays).forEach(([key, holiday]) => {
        const holidayStart = new Date(holiday.start);
        const diff = holidayStart - today;
        
        if (diff > 0 && diff < minDiff) {
            minDiff = diff;
            nextHoliday = { key, ...holiday };
        }
    });
    
    return nextHoliday;
}

/**
 * Find holiday by search term (e.g., "october half term", "easter")
 * @param {string} searchTerm - Search term
 * @param {string} council - Council name
 * @returns {Object} Holiday information
 */
function findHolidayByTerm(searchTerm, council = null) {
    const holidays = getSchoolHolidays(council);
    const term = searchTerm.toLowerCase();
    
    // Direct key match
    if (holidays[term]) {
        return holidays[term];
    }
    
    // Search in holiday names
    for (const [key, holiday] of Object.entries(holidays)) {
        if (holiday.name.toLowerCase().includes(term) || 
            key.includes(term.replace(/\s+/g, '-'))) {
            return holiday;
        }
    }
    
    return null;
}

/**
 * Get all school holidays for the year
 * @param {string} council - Council name
 * @returns {Array} All holidays sorted by date
 */
function getAllSchoolHolidays(council = null) {
    const holidays = getSchoolHolidays(council);
    
    return Object.entries(holidays)
        .map(([key, holiday]) => ({ key, ...holiday }))
        .sort((a, b) => new Date(a.start) - new Date(b.start));
}

/**
 * Check if a date falls within school holidays
 * @param {Date|string} date - Date to check
 * @param {string} council - Council name
 * @returns {Object|null} Holiday information if date is in holidays
 */
function isSchoolHoliday(date, council = null) {
    const holidays = getSchoolHolidays(council);
    const checkDate = new Date(date);
    
    for (const [key, holiday] of Object.entries(holidays)) {
        const start = new Date(holiday.start);
        const end = new Date(holiday.end);
        
        if (checkDate >= start && checkDate <= end) {
            return { key, ...holiday };
        }
    }
    
    return null;
}

/**
 * Suggest optimal travel dates around school holidays
 * @param {string} holidayKey - Holiday key (e.g., 'easter-holidays')
 * @param {string} council - Council name
 * @returns {Object} Suggested travel dates
 */
function suggestTravelDates(holidayKey, council = null) {
    const holidays = getSchoolHolidays(council);
    const holiday = holidays[holidayKey];
    
    if (!holiday) return null;
    
    const startDate = new Date(holiday.start);
    const endDate = new Date(holiday.end);
    
    // Suggest a few days before and after for better prices
    const earlyStart = new Date(startDate);
    earlyStart.setDate(startDate.getDate() - 2);
    
    const lateEnd = new Date(endDate);
    lateEnd.setDate(endDate.getDate() + 2);
    
    return {
        holiday: holiday,
        exact: {
            start: holiday.start,
            end: holiday.end,
            description: `Exact ${holiday.name} dates`
        },
        early: {
            start: earlyStart.toISOString().split('T')[0],
            end: holiday.end,
            description: `Start 2 days early for better prices`
        },
        extended: {
            start: holiday.start,
            end: lateEnd.toISOString().split('T')[0],
            description: `Extend 2 days for better value`
        }
    };
}

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        getSchoolHolidays,
        getNextSchoolHoliday,
        findHolidayByTerm,
        getAllSchoolHolidays,
        isSchoolHoliday,
        suggestTravelDates,
        UK_SCHOOL_HOLIDAYS_2025,
        COUNCIL_VARIATIONS
    };
}