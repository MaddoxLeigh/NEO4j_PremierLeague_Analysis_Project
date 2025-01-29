UNWIND $venues AS venue
MATCH (v:Venue {name: venue.venue_name})
SET v.capacity = venue.capacity
