/*
This query is used to insert venue capacity attribute to each venue we have on the instance.

It does this by taking a list of dictionaries, each with a venue name and capcity key and then finds the respecitive venue and sets the value.
*/

UNWIND $venues AS venue
MATCH (v:Venue {name: venue.venue_name})
SET v.capacity = toInteger(venue.venue_capacity)
