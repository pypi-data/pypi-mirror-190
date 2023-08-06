## interzoid_address_match_key

Python package for generating a similarity key from the input data used to match with other similar street address data. Use the generated similarity key, rather than the actual data itself, to match and/or sort street address data by similarity. This avoids the problems of data inconsistency, misspellings, and address element variations when matching within a single dataset, and can also help matching across datasets or for more advanced searching.

The key generation is based on a series of tests, algorithms, AI, and an ever-growing body of Machine Learning-based generated knowledge.

### Usage

To generate the similarity key, you will need the following information:

- an API License key, available at https://www.interzoid.com
- a street address to generate the similarity key for

An API is called by the package to access the Cloud server that generates the similarity key.

Begin by importing the package:

    from interzoid_address_match_key import address_match_key

Then, provide the information into the get_key() method:

    sim_key, credits, http_code, msg = address_match_key.get_key('YOUR-API-KEY','107 E. Main St.')

    #200 is the HTTP status for OK
    if http_code == 200:  
        print(sim_key, msg, credits)
    else:
        print(sim_key, "error:", http_code, msg, credits)

The return values will be the generated similarity key, a code (success or failure), how many remaining credits on your API key, and any error messages. The similarity key can be used to search for other similar street addresses, to sort large datasets by similarity, and perhaps use additional attributes to identify duplicates/redundancy.

Examples:

    100 E. Main St. Suite 101  ->  fS9Xxx-9HoRD4ZGJA43meLBS3tAn5YjdCClGJyXtUrw
    100 East Main St. #101  ->  fS9Xxx-9HoRD4ZGJA43meLBS3tAn5YjdCClGJyXtUrw

    Park Avenue #500  ->   EP88bx0VFDaIh-cOt86c8pOJ6lNkb_TWiKFpmMKXakY
    500 PARK AVE.  ->  EP88bx0VFDaIh-cOt86c8pOJ6lNkb_TWiKFpmMKXakY