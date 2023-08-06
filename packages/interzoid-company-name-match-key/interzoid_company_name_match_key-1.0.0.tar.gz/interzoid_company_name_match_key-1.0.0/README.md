## interzoid_company_name_match_key

Python package for generating a similarity key from the input data used to match with other similar company name data. Use the generated similarity key, rather than the actual data itself, to match and/or sort company name data by similarity. This avoids the problems of data inconsistency, misspellings, and name variations when matching within a single dataset, and can also help matching across datasets or for more advanced searching.

The key generation is based on a series of tests, algorithms, AI, and an ever-growing body of Machine Learning-based generated knowledge.  As the context of the data is known, in this case organization/company names, it performs far better than generic string comparison algorithms.

### Usage

To generate the similarity key, you will need the following information:

- an API License key, available at https://www.interzoid.com
- a company name to generate the similarity key for

An API is called by the package to access the Cloud server that generates the similarity key.

Begin by importing the package:

    from interzoid_company_name_match_key import company_name_match_key

Then, provide the information into the get_key() method:

    sim_key, credits, http_code, msg = company_name_match_key.get_key('YOUR-API-KEY','Bank of America')

    #200 is the HTTP status for OK
    if http_code == 200:  
        print(sim_key, msg, credits)
    else:
        print(sim_key, "error:", http_code, msg, credits)

The return values will be the generated similarity key, a code (success or failure), how many remaining credits on your API key, and any error messages. The similarity key can be used to search for other similar company names, to sort large datasets by similarity, and perhaps use additional attributes to identify duplicates/redundancy.

Examples:

    Bank of America  ->  wAR3laPfUVvB784_iH0cw7aQbKhr26sophlZ4z7iqtM
    Bank of Amer Corp  ->  wAR3laPfUVvB784_iH0cw7aQbKhr26sophlZ4z7iqtM

    AMAZON.COM  ->   EP88bx0VFDaIh-cOt86c8pOJ6lNkb_TWiKFpmMKXakY
    Amazon Inc.  ->  EP88bx0VFDaIh-cOt86c8pOJ6lNkb_TWiKFpmMKXakY