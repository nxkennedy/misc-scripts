# we know that there are 72 domains we're looking for (cheating)
# for every 12 domains, print a query (72 / 12 = 6 queries)(this is
# because google has search length limitations)
# we take the queries this spits out and paste them into google and look at the results
query = 'allinurl:(".gov/" "?url=") inurl:('
with open('domains.txt', 'r') as f:
    domain_count = 0
    acceptable_length = 12
    for site in f:
        domain_count += 1

        if domain_count == acceptable_length:
            domain_count = 0
            query += site.strip() + ') "porn OR xxx OR nude"'
            print query
            print
            query = 'allinurl:(".gov/" "?url=") inurl:('

        else:
            query += site.strip() + ' OR '
