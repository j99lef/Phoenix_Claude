# How TravelAiGent Finds Complete Travel Packages

## Current Implementation

TravelAiGent is designed to find **complete travel packages** including both flights and accommodation:

### 1. **Package Search Process**
When you create a travel brief, the system:
```
Travel Brief → Flight Search → Hotel Search → Combined Package
```

### 2. **What Gets Searched**

#### Flights (via Amadeus Flight API)
- Searches multiple departure airports (e.g., LHR, LGW, STN)
- Filters by your budget
- Considers your travel dates
- Looks for family-friendly airlines

#### Hotels (via Amadeus Hotel API)
- **Only 4-5 star hotels** (as per luxury travel requirements)
- Family-friendly properties with amenities:
  - Pool
  - WiFi
  - Restaurant
  - Family plans
- Within 20km of destination center
- Sorted by best value

### 3. **Package Creation**
The system combines the best flight + best hotel to create packages:
```json
{
  "type": "package",
  "destination": "PAR",
  "total_price": 2500,  // Flight + Hotel combined
  "flight_price": 800,
  "hotel_price": 1700,
  "hotel_name": "Premium Family Resort",
  "hotel_rating": "5 stars",
  "room_type": "Family Room",
  "duration_nights": 7,
  "savings": 300  // vs booking separately
}
```

### 4. **Deal Types in the System**

1. **Complete Packages** (Flight + Hotel)
   - Primary offering
   - Best value with package savings
   - Single booking reference

2. **Flight-Only Deals**
   - Fallback when no suitable hotels found
   - For destinations where you might have accommodation

3. **Hotel-Only Deals**
   - For staycations or drive-to destinations
   - When flights aren't needed

### 5. **How to Enable Full Package Search**

With your Amadeus credentials now added:
1. Create a travel brief specifying:
   - Destination
   - Travel dates
   - Budget (this will be split between flight and hotel)
   - Number of travelers

2. The system will automatically:
   - Search for flights from your home airports
   - Find 4-5 star family hotels at the destination
   - Create packages with total pricing
   - Show savings vs separate booking

### 6. **Booking Process**
- TravelAiGent finds and presents the packages
- When you click "Book Now", you're redirected to:
  - Amadeus booking portal
  - Partner travel sites
  - Direct airline/hotel websites
- You complete the actual booking on their platforms

### 7. **Why Packages?**
- **Better Value**: Package deals often have discounts
- **Convenience**: One search finds everything
- **Quality Assured**: Only premium accommodations
- **Family-Focused**: All results are family-friendly

## Testing Your Setup

Now that Amadeus is configured, try creating a travel brief:
1. Destination: "Paris" or "Barcelona"
2. Dates: 30-60 days from now
3. Budget: £2000-3000 per person
4. Travelers: Your family group

The system will search for complete packages and show them in your deals list!