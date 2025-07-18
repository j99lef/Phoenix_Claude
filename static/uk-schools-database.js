/**
 * UK Schools and Councils Database
 * Comprehensive database of UK schools and local authorities with term dates
 */

// Major UK Local Education Authorities with their term dates (2025)
const UK_LOCAL_AUTHORITIES = {
    // England - London Boroughs
    'barking-and-dagenham': {
        name: 'Barking and Dagenham',
        region: 'London',
        country: 'England',
        holidays: {
            'spring-half-term': { start: '2025-02-17', end: '2025-02-21', type: 'half-term' },
            'easter-holidays': { start: '2025-04-14', end: '2025-04-25', type: 'main-holiday' },
            'may-half-term': { start: '2025-05-26', end: '2025-05-30', type: 'half-term' },
            'summer-holidays': { start: '2025-07-21', end: '2025-09-01', type: 'main-holiday' },
            'autumn-half-term': { start: '2025-10-27', end: '2025-10-31', type: 'half-term' },
            'christmas-holidays': { start: '2025-12-19', end: '2026-01-06', type: 'main-holiday' }
        },
        insetDays: [
            { date: '2025-01-06', type: 'start-of-term', opportunity: 'extended-weekend' },
            { date: '2025-02-14', type: 'pre-half-term', opportunity: 'long-weekend' },
            { date: '2025-04-11', type: 'pre-easter', opportunity: 'extended-break' },
            { date: '2025-05-23', type: 'pre-half-term', opportunity: 'long-weekend' },
            { date: '2025-07-18', type: 'pre-summer', opportunity: 'extended-break' },
            { date: '2025-09-02', type: 'start-of-term', opportunity: 'extended-weekend' }
        ]
    },
    'camden': {
        name: 'Camden',
        region: 'London',
        country: 'England',
        holidays: {
            'spring-half-term': { start: '2025-02-17', end: '2025-02-21' },
            'easter-holidays': { start: '2025-04-14', end: '2025-04-25' },
            'may-half-term': { start: '2025-05-26', end: '2025-05-30' },
            'summer-holidays': { start: '2025-07-21', end: '2025-09-01' },
            'autumn-half-term': { start: '2025-10-27', end: '2025-10-31' },
            'christmas-holidays': { start: '2025-12-22', end: '2026-01-05' }
        }
    },
    'westminster': {
        name: 'Westminster',
        region: 'London',
        country: 'England',
        holidays: {
            'spring-half-term': { start: '2025-02-17', end: '2025-02-21' },
            'easter-holidays': { start: '2025-04-11', end: '2025-04-25' },
            'may-half-term': { start: '2025-05-26', end: '2025-05-30' },
            'summer-holidays': { start: '2025-07-18', end: '2025-09-01' },
            'autumn-half-term': { start: '2025-10-27', end: '2025-10-31' },
            'christmas-holidays': { start: '2025-12-19', end: '2026-01-06' }
        }
    },
    
    // England - Major Cities
    'birmingham': {
        name: 'Birmingham',
        region: 'West Midlands',
        country: 'England',
        holidays: {
            'spring-half-term': { start: '2025-02-17', end: '2025-02-21', type: 'half-term' },
            'easter-holidays': { start: '2025-04-14', end: '2025-04-25', type: 'main-holiday' },
            'may-half-term': { start: '2025-05-26', end: '2025-05-30', type: 'half-term' },
            'summer-holidays': { start: '2025-07-21', end: '2025-09-01', type: 'main-holiday' },
            'autumn-half-term': { start: '2025-10-27', end: '2025-10-31', type: 'half-term' },
            'christmas-holidays': { start: '2025-12-20', end: '2026-01-06', type: 'main-holiday' }
        },
        insetDays: [
            { date: '2025-01-06', type: 'start-of-term', opportunity: 'extended-weekend' },
            { date: '2025-02-14', type: 'pre-half-term', opportunity: 'long-weekend' },
            { date: '2025-04-11', type: 'pre-easter', opportunity: 'extended-break' },
            { date: '2025-05-23', type: 'pre-half-term', opportunity: 'long-weekend' },
            { date: '2025-07-18', type: 'pre-summer', opportunity: 'extended-break' },
            { date: '2025-09-02', type: 'start-of-term', opportunity: 'extended-weekend' }
        ]
    },
    'manchester': {
        name: 'Manchester',
        region: 'Greater Manchester',
        country: 'England',
        holidays: {
            'spring-half-term': { start: '2025-02-17', end: '2025-02-21' },
            'easter-holidays': { start: '2025-04-14', end: '2025-04-25' },
            'may-half-term': { start: '2025-05-26', end: '2025-05-30' },
            'summer-holidays': { start: '2025-07-21', end: '2025-09-01' },
            'autumn-half-term': { start: '2025-10-27', end: '2025-10-31' },
            'christmas-holidays': { start: '2025-12-22', end: '2026-01-05' }
        }
    },
    'leeds': {
        name: 'Leeds',
        region: 'West Yorkshire',
        country: 'England',
        holidays: {
            'spring-half-term': { start: '2025-02-17', end: '2025-02-21' },
            'easter-holidays': { start: '2025-04-14', end: '2025-04-25' },
            'may-half-term': { start: '2025-05-26', end: '2025-05-30' },
            'summer-holidays': { start: '2025-07-21', end: '2025-09-01' },
            'autumn-half-term': { start: '2025-10-27', end: '2025-10-31' },
            'christmas-holidays': { start: '2025-12-19', end: '2026-01-06' }
        }
    },
    'liverpool': {
        name: 'Liverpool',
        region: 'Merseyside',
        country: 'England',
        holidays: {
            'spring-half-term': { start: '2025-02-17', end: '2025-02-21' },
            'easter-holidays': { start: '2025-04-14', end: '2025-04-25' },
            'may-half-term': { start: '2025-05-26', end: '2025-05-30' },
            'summer-holidays': { start: '2025-07-21', end: '2025-09-01' },
            'autumn-half-term': { start: '2025-10-27', end: '2025-10-31' },
            'christmas-holidays': { start: '2025-12-22', end: '2026-01-05' }
        }
    },
    
    // Scotland
    'edinburgh': {
        name: 'Edinburgh',
        region: 'Scotland',
        country: 'Scotland',
        holidays: {
            'february-break': { start: '2025-02-10', end: '2025-02-14' },
            'spring-break': { start: '2025-04-07', end: '2025-04-18' },
            'may-break': { start: '2025-05-19', end: '2025-05-23' },
            'summer-holidays': { start: '2025-06-30', end: '2025-08-18' },
            'october-break': { start: '2025-10-13', end: '2025-10-17' },
            'christmas-holidays': { start: '2025-12-22', end: '2026-01-07' }
        }
    },
    'glasgow': {
        name: 'Glasgow',
        region: 'Scotland',
        country: 'Scotland',
        holidays: {
            'february-break': { start: '2025-02-10', end: '2025-02-14' },
            'spring-break': { start: '2025-04-07', end: '2025-04-18' },
            'may-break': { start: '2025-05-19', end: '2025-05-23' },
            'summer-holidays': { start: '2025-06-30', end: '2025-08-18' },
            'october-break': { start: '2025-10-13', end: '2025-10-17' },
            'christmas-holidays': { start: '2025-12-22', end: '2026-01-07' }
        }
    },
    
    // Wales
    'cardiff': {
        name: 'Cardiff',
        region: 'Wales',
        country: 'Wales',
        holidays: {
            'spring-half-term': { start: '2025-02-17', end: '2025-02-21' },
            'easter-holidays': { start: '2025-04-14', end: '2025-04-25' },
            'may-half-term': { start: '2025-05-26', end: '2025-05-30' },
            'summer-holidays': { start: '2025-07-21', end: '2025-09-01' },
            'autumn-half-term': { start: '2025-10-27', end: '2025-10-31' },
            'christmas-holidays': { start: '2025-12-20', end: '2026-01-06' }
        }
    },
    'swansea': {
        name: 'Swansea',
        region: 'Wales',
        country: 'Wales',
        holidays: {
            'spring-half-term': { start: '2025-02-17', end: '2025-02-21' },
            'easter-holidays': { start: '2025-04-14', end: '2025-04-25' },
            'may-half-term': { start: '2025-05-26', end: '2025-05-30' },
            'summer-holidays': { start: '2025-07-21', end: '2025-09-01' },
            'autumn-half-term': { start: '2025-10-27', end: '2025-10-31' },
            'christmas-holidays': { start: '2025-12-20', end: '2026-01-06' }
        }
    },
    
    // Northern Ireland
    'belfast': {
        name: 'Belfast',
        region: 'Northern Ireland',
        country: 'Northern Ireland',
        holidays: {
            'spring-break': { start: '2025-03-17', end: '2025-03-21' },
            'easter-holidays': { start: '2025-04-14', end: '2025-04-25' },
            'summer-holidays': { start: '2025-07-01', end: '2025-08-29' },
            'autumn-half-term': { start: '2025-10-27', end: '2025-10-31' },
            'christmas-holidays': { start: '2025-12-22', end: '2026-01-02' }
        }
    }
};

// Major UK Independent Schools with specific term dates
const UK_INDEPENDENT_SCHOOLS = {
    'eton-college': {
        name: 'Eton College',
        type: 'Independent',
        region: 'Berkshire',
        country: 'England',
        holidays: {
            'lent-half-term': { start: '2025-02-15', end: '2025-02-23' },
            'easter-holidays': { start: '2025-04-11', end: '2025-04-29' },
            'summer-half-term': { start: '2025-05-24', end: '2025-06-02' },
            'summer-holidays': { start: '2025-07-11', end: '2025-09-08' },
            'autumn-half-term': { start: '2025-10-18', end: '2025-11-02' },
            'christmas-holidays': { start: '2025-12-13', end: '2026-01-13' }
        }
    },
    'harrow-school': {
        name: 'Harrow School',
        type: 'Independent',
        region: 'London',
        country: 'England',
        holidays: {
            'lent-half-term': { start: '2025-02-15', end: '2025-02-23' },
            'easter-holidays': { start: '2025-04-11', end: '2025-04-29' },
            'summer-half-term': { start: '2025-05-24', end: '2025-06-02' },
            'summer-holidays': { start: '2025-07-11', end: '2025-09-08' },
            'autumn-half-term': { start: '2025-10-18', end: '2025-11-02' },
            'christmas-holidays': { start: '2025-12-13', end: '2026-01-13' }
        }
    },
    'winchester-college': {
        name: 'Winchester College',
        type: 'Independent',
        region: 'Hampshire',
        country: 'England',
        holidays: {
            'lent-half-term': { start: '2025-02-15', end: '2025-02-23' },
            'easter-holidays': { start: '2025-04-11', end: '2025-04-29' },
            'summer-half-term': { start: '2025-05-24', end: '2025-06-02' },
            'summer-holidays': { start: '2025-07-11', end: '2025-09-08' },
            'autumn-half-term': { start: '2025-10-18', end: '2025-11-02' },
            'christmas-holidays': { start: '2025-12-13', end: '2026-01-13' }
        }
    }
};

// Combined database
const UK_SCHOOLS_DATABASE = {
    ...UK_LOCAL_AUTHORITIES,
    ...UK_INDEPENDENT_SCHOOLS
};

/**
 * Search for schools/councils by name or region
 * @param {string} query - Search query
 * @returns {Array} Array of matching schools/councils
 */
function searchSchools(query) {
    if (!query || query.length < 2) return [];
    
    const searchTerm = query.toLowerCase();
    const results = [];
    
    Object.entries(UK_SCHOOLS_DATABASE).forEach(([key, school]) => {
        const nameMatch = school.name.toLowerCase().includes(searchTerm);
        const regionMatch = school.region && school.region.toLowerCase().includes(searchTerm);
        const countryMatch = school.country.toLowerCase().includes(searchTerm);
        
        if (nameMatch || regionMatch || countryMatch) {
            results.push({
                key,
                ...school,
                matchType: nameMatch ? 'name' : regionMatch ? 'region' : 'country'
            });
        }
    });
    
    // Sort by relevance (name matches first, then region, then country)
    return results.sort((a, b) => {
        const order = { name: 1, region: 2, country: 3 };
        return order[a.matchType] - order[b.matchType];
    });
}

/**
 * Get school/council holidays by key
 * @param {string} schoolKey - School/council key
 * @returns {Object} Holiday dates
 */
function getSchoolHolidays(schoolKey) {
    const school = UK_SCHOOLS_DATABASE[schoolKey];
    return school ? school.holidays : null;
}

/**
 * Get school/council information by key
 * @param {string} schoolKey - School/council key
 * @returns {Object} School information
 */
function getSchoolInfo(schoolKey) {
    return UK_SCHOOLS_DATABASE[schoolKey] || null;
}

/**
 * Get all available schools/councils
 * @returns {Array} All schools/councils
 */
function getAllSchools() {
    return Object.entries(UK_SCHOOLS_DATABASE).map(([key, school]) => ({
        key,
        ...school
    }));
}

/**
 * Get schools by region
 * @param {string} region - Region name
 * @returns {Array} Schools in the region
 */
function getSchoolsByRegion(region) {
    return Object.entries(UK_SCHOOLS_DATABASE)
        .filter(([_, school]) => school.region && school.region.toLowerCase() === region.toLowerCase())
        .map(([key, school]) => ({ key, ...school }));
}

/**
 * Get schools by country
 * @param {string} country - Country name
 * @returns {Array} Schools in the country
 */
function getSchoolsByCountry(country) {
    return Object.entries(UK_SCHOOLS_DATABASE)
        .filter(([_, school]) => school.country.toLowerCase() === country.toLowerCase())
        .map(([key, school]) => ({ key, ...school }));
}

/**
 * Get upcoming holidays for a specific school
 * @param {string} schoolKey - School key
 * @param {number} months - Number of months ahead to look
 * @returns {Array} Upcoming holidays
 */
function getUpcomingHolidays(schoolKey, months = 12) {
    const school = UK_SCHOOLS_DATABASE[schoolKey];
    if (!school) return [];
    
    const today = new Date();
    const futureDate = new Date();
    futureDate.setMonth(today.getMonth() + months);
    
    return Object.entries(school.holidays)
        .map(([key, holiday]) => ({
            key,
            name: key.replace(/-/g, ' ').replace(/\b\w/g, l => l.toUpperCase()),
            ...holiday
        }))
        .filter(holiday => {
            const holidayDate = new Date(holiday.start);
            return holidayDate >= today && holidayDate <= futureDate;
        })
        .sort((a, b) => new Date(a.start) - new Date(b.start));
}

/**
 * Find holiday by name for a specific school
 * @param {string} schoolKey - School key
 * @param {string} holidayName - Holiday name or key
 * @returns {Object} Holiday information
 */
function findHolidayByName(schoolKey, holidayName) {
    const school = UK_SCHOOLS_DATABASE[schoolKey];
    if (!school) return null;
    
    const searchTerm = holidayName.toLowerCase().replace(/\s+/g, '-');
    
    // Direct key match
    if (school.holidays[searchTerm]) {
        return {
            key: searchTerm,
            name: searchTerm.replace(/-/g, ' ').replace(/\b\w/g, l => l.toUpperCase()),
            ...school.holidays[searchTerm]
        };
    }
    
    // Search in holiday keys
    for (const [key, holiday] of Object.entries(school.holidays)) {
        if (key.includes(searchTerm) || searchTerm.includes(key)) {
            return {
                key,
                name: key.replace(/-/g, ' ').replace(/\b\w/g, l => l.toUpperCase()),
                ...holiday
            };
        }
    }
    
    return null;
}

/**
 * Get INSET days for a specific school
 * @param {string} schoolKey - School key
 * @returns {Array} INSET days
 */
function getInsetDays(schoolKey) {
    const school = UK_SCHOOLS_DATABASE[schoolKey];
    return school && school.insetDays ? school.insetDays : [];
}

/**
 * Get weekend getaway opportunities (INSET days that create long weekends)
 * @param {string} schoolKey - School key
 * @param {number} months - Number of months ahead to look
 * @returns {Array} Weekend getaway opportunities
 */
function getWeekendGetawayOpportunities(schoolKey, months = 6) {
    const school = UK_SCHOOLS_DATABASE[schoolKey];
    if (!school || !school.insetDays) return [];
    
    const today = new Date();
    const futureDate = new Date();
    futureDate.setMonth(today.getMonth() + months);
    
    return school.insetDays
        .filter(insetDay => {
            const insetDate = new Date(insetDay.date);
            return insetDate >= today && insetDate <= futureDate;
        })
        .map(insetDay => {
            const insetDate = new Date(insetDay.date);
            const dayOfWeek = insetDate.getDay();
            
            let opportunity = {
                ...insetDay,
                dayOfWeek: ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'][dayOfWeek],
                dealType: 'weekend-getaway'
            };
            
            // Determine the type of opportunity
            if (dayOfWeek === 1) { // Monday
                opportunity.description = 'Monday INSET day creates 3-day weekend';
                opportunity.suggestedDuration = '3 days';
                opportunity.marketingMessage = 'Long Weekend Deal';
            } else if (dayOfWeek === 5) { // Friday
                opportunity.description = 'Friday INSET day creates 3-day weekend';
                opportunity.suggestedDuration = '3 days';
                opportunity.marketingMessage = 'Extended Weekend Escape';
            } else if (dayOfWeek === 4) { // Thursday
                opportunity.description = 'Thursday INSET day - perfect for city breaks';
                opportunity.suggestedDuration = '2-3 days';
                opportunity.marketingMessage = 'Midweek City Break';
            } else if (dayOfWeek === 2) { // Tuesday
                opportunity.description = 'Tuesday INSET day - great for short breaks';
                opportunity.suggestedDuration = '2 days';
                opportunity.marketingMessage = 'Tuesday Getaway';
            }
            
            return opportunity;
        })
        .sort((a, b) => new Date(a.date) - new Date(b.date));
}

/**
 * Get all extended break opportunities (INSET days + holidays)
 * @param {string} schoolKey - School key
 * @param {number} months - Number of months ahead to look
 * @returns {Array} Extended break opportunities
 */
function getExtendedBreakOpportunities(schoolKey, months = 12) {
    const school = UK_SCHOOLS_DATABASE[schoolKey];
    if (!school) return [];
    
    const opportunities = [];
    const today = new Date();
    const futureDate = new Date();
    futureDate.setMonth(today.getMonth() + months);
    
    // Check for INSET days that extend holidays
    if (school.insetDays) {
        school.insetDays.forEach(insetDay => {
            if (insetDay.opportunity === 'extended-break') {
                const insetDate = new Date(insetDay.date);
                if (insetDate >= today && insetDate <= futureDate) {
                    
                    // Find the associated holiday
                    const associatedHoliday = Object.entries(school.holidays).find(([key, holiday]) => {
                        const holidayStart = new Date(holiday.start);
                        const holidayEnd = new Date(holiday.end);
                        const daysBetween = Math.abs(insetDate - holidayStart) / (1000 * 60 * 60 * 24);
                        return daysBetween <= 3; // INSET day within 3 days of holiday
                    });
                    
                    if (associatedHoliday) {
                        const [holidayKey, holiday] = associatedHoliday;
                        opportunities.push({
                            type: 'extended-break',
                            insetDay: insetDay,
                            holiday: {
                                key: holidayKey,
                                name: holidayKey.replace(/-/g, ' ').replace(/\b\w/g, l => l.toUpperCase()),
                                ...holiday
                            },
                            description: `INSET day extends ${holidayKey.replace(/-/g, ' ')}`,
                            marketingMessage: 'Extended Holiday Break',
                            dealType: 'extended-holiday'
                        });
                    }
                }
            }
        });
    }
    
    return opportunities.sort((a, b) => new Date(a.insetDay.date) - new Date(b.insetDay.date));
}

/**
 * Get all bonus travel opportunities for a school
 * @param {string} schoolKey - School key
 * @param {number} months - Number of months ahead to look
 * @returns {Object} All travel opportunities
 */
function getBonusTravelOpportunities(schoolKey, months = 12) {
    return {
        weekendGetaways: getWeekendGetawayOpportunities(schoolKey, months),
        extendedBreaks: getExtendedBreakOpportunities(schoolKey, months),
        upcomingHolidays: getUpcomingHolidays(schoolKey, months)
    };
}

/**
 * Check if a date is an INSET day
 * @param {string} schoolKey - School key
 * @param {Date|string} date - Date to check
 * @returns {Object|null} INSET day information if found
 */
function isInsetDay(schoolKey, date) {
    const school = UK_SCHOOLS_DATABASE[schoolKey];
    if (!school || !school.insetDays) return null;
    
    const checkDate = new Date(date).toISOString().split('T')[0];
    
    return school.insetDays.find(insetDay => insetDay.date === checkDate) || null;
}

/**
 * Get marketing messages for deals based on school calendar
 * @param {string} schoolKey - School key
 * @param {Date|string} travelDate - Travel date
 * @returns {Object} Marketing suggestions
 */
function getMarketingMessages(schoolKey, travelDate) {
    const school = UK_SCHOOLS_DATABASE[schoolKey];
    if (!school) return null;
    
    const date = new Date(travelDate);
    const dateString = date.toISOString().split('T')[0];
    
    // Check if it's an INSET day
    const insetDay = isInsetDay(schoolKey, date);
    if (insetDay) {
        return {
            type: 'inset-day',
            message: insetDay.marketingMessage || 'INSET Day Special',
            description: insetDay.description,
            dealType: 'bonus-weekend',
            urgency: 'high'
        };
    }
    
    // Check if it's during school holidays
    for (const [key, holiday] of Object.entries(school.holidays)) {
        const holidayStart = new Date(holiday.start);
        const holidayEnd = new Date(holiday.end);
        
        if (date >= holidayStart && date <= holidayEnd) {
            return {
                type: 'school-holiday',
                message: `${key.replace(/-/g, ' ').replace(/\b\w/g, l => l.toUpperCase())} Deal`,
                description: `Perfect for ${holiday.type === 'half-term' ? 'half-term' : 'holiday'} travel`,
                dealType: holiday.type,
                urgency: 'medium'
            };
        }
    }
    
    return {
        type: 'term-time',
        message: 'Term-time Savings',
        description: 'Great value during school term',
        dealType: 'standard',
        urgency: 'low'
    };
}

// Export for use in other modules
// Export for Node.js if available
if (typeof module !== 'undefined' && module.exports) {
        module.exports = {
            UK_SCHOOLS_DATABASE,
            UK_LOCAL_AUTHORITIES,
            UK_INDEPENDENT_SCHOOLS,
            searchSchools,
            getSchoolHolidays,
            getSchoolInfo,
            getAllSchools,
            getSchoolsByRegion,
            getSchoolsByCountry,
            getUpcomingHolidays,
            findHolidayByName,
            getInsetDays,
            getWeekendGetawayOpportunities,
            getExtendedBreakOpportunities,
            getBonusTravelOpportunities,
            isInsetDay,
            getMarketingMessages
        };
}

// Export for browser if available
if (typeof window !== 'undefined') {
        window.getSchoolInfo = getSchoolInfo;
        window.searchSchools = searchSchools;
        window.getSchoolHolidays = getSchoolHolidays;
        window.getAllSchools = getAllSchools;
        window.getSchoolsByRegion = getSchoolsByRegion;
        window.getSchoolsByCountry = getSchoolsByCountry;
        window.getUpcomingHolidays = getUpcomingHolidays;
        window.findHolidayByName = findHolidayByName;
        window.getInsetDays = getInsetDays;
        window.getWeekendGetawayOpportunities = getWeekendGetawayOpportunities;
        window.getExtendedBreakOpportunities = getExtendedBreakOpportunities;
        window.getBonusTravelOpportunities = getBonusTravelOpportunities;
        window.isInsetDay = isInsetDay;
        window.getMarketingMessages = getMarketingMessages;
    }
}