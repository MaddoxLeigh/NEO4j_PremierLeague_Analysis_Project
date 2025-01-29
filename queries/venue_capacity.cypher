UNWIND $venues AS venue
MATCH (v:Venue {name: venue.venue_name})
SET v.capacity = toInteger(venue.venue_capacity)
