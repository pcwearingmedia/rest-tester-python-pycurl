"""Use pycurl to perform HTTP request tests on web sites or REST APIs."""
#!/usr/bin/python

# Author: P-C Markovski
# Version: 1.0

import pymysql, pycurl, csv, sys, warnings

    # Setup the database table structure.

def dbsetup():
    """Create a database connection and return the connection handle and the cursor."""
    
        # Python inner function: Create a table if it does not exist.
    def zint_createtable(dbconn):
        """ Create the database table for the load test metrics if the table does not exist."""
        try:
            with dbconn.cursor() as cursor:
                sql = "create table if not exists loadmetrics(responsecode varchar(50), rtt varchar(50), url varchar(500))"
                cursor.execute(sql)
        except pymysql.InternalError as e:
            code, message = e.args

	
    try:
        con = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='LookYonder!', db='restapitests', autocommit=True)
    except pymysql.InternalError as e:
        code, message = e.args
        print(">>>", code, message)
        sys.exit()

    # Create the table to store statistics, iff it doesn't already exist.
    zint_createtable(con)

    cr = con.cursor()
    return con, cr


    # Close the database connection and cursor.

def dbclose(dbconn, crconn):
    """Close the database connection handle and the cursor."""
    
    crconn.close()
    dbconn.close()

    print("Database closed.")
    
    return True


    # List the statistics stored in the database table.

def liststatistics(dbconn):
    """List the existing load test metrics that exist in the database table."""
	
    try:
        with dbconn.cursor() as cursor:
            sql = "select * from loadmetrics"
            cursor.execute(sql)
            for row in cursor:
                print(row)
			
    except pymysql.InternalError as e:
        code, message = e.args
        print(">>>", code, message)
        
    return True


    # Add a new record with HTTP request statistics to the database table.

def addrecords(dbconn, ret_responsecode, ret_rtt, url):
    """Add the most recent load test metrics to the database table."""

    try:
        with dbconn.cursor() as cursor:
            sql = "insert into loadmetrics (responsecode, rtt, url) values(%s,%s,%s)"
            cursor.execute(sql, (ret_responsecode, ret_rtt, url))
    except pymysql.InternalError as e:
        code, message = e.args
        print(">>>", code, message)
        
    return True
    
    

    # Run a HTTP request with the Curl package.

def httprequest(url, reqtype, json):
    """Perform a HTTP request."""
	
    c = pycurl.Curl()
    c.setopt(c.URL, url)
    c.setopt(c.FOLLOWLOCATION, True)
    c.perform()

        # Add metrics to measure.
    response = c.getinfo(c.RESPONSE_CODE)
    rtt = c.getinfo(c.TOTAL_TIME)

    c.close()

    return response, rtt

    # Load the requests from a CSV file into a list and return the list.

def loadrequests(csvfile):
    """Load HTTP request commands that are stored in a CSV file."""
	
    try:
        with open(csvfile, 'r') as f:
            reader = csv.reader(f)
            lstRequests = list(reader)
			
    except IOError as e:
        code, message = e.args
        print(">>>", code, message)

    # The file should be closed here..

    return lstRequests



    #
    # Program logic.
    # Connect to the database.
    # Use if statements to check the arguments sent to the script.
    #

    # Insert a line into the Warnings filter. Don't print warnings.
warnings.simplefilter("ignore")


    # No parameters passed.

if len(sys.argv) <= 1:
    print('\nPlease provide one of the following options.')
    print('list - List stored statistics.')
    print('single <URL> - Test one website page.')
    print('multiple - Load multiple website pages that are stored in requests.csv. Run a test against each.\n')
    sys.exit()


    # Connect to the database, save the connection handle and cursor for the program branches to use.
    # The database table will be cratead iff it doesn't exist.

tmpCON, tmpCR = dbsetup()

    # One parameter passed.
    # List stored statistics: If "list" is passed to the script.
    # This relies on the database connection handle and cursor.

if len(sys.argv) == 2:
    if sys.argv[1] == "list":
        liststatistics(tmpCON)
        sys.exit()
    sys.exit()

    # Run multiple requests, based on the play list in CSV format.
    # Run the CURL request for the site, add the stats to the database, close the db.

    # Two parameters passed.

if len(sys.argv) == 3:

    # Single GET request on an URL.

    if sys.argv[1] == "single":

        # ToDo: Validate the format of the passed URL (argument 1).
        print('Checking %s' % sys.argv[2])

        re, rttime = httprequest(sys.argv[2], 'GET', '-')
        addrecords(tmpCON, re, rttime, sys.argv[2])
        dbclose(tmpCR, tmpCON)

        # Print the last http request results to verify that the http request worked.
        print('Status: %d' % re)
        print('Round-trip time: %f' % rttime)
        sys.exit()

    # Multiple requests.

    if sys.argv[1] == "multiple":
        lst = loadrequests(sys.argv[2])

            # For each entry in the list, perform curl request and store result in the database.
        for entry in lst:
            re, rttime = httprequest(entry[0], 'GET', '-') # ToDo: Use entry[1] to specify the HTTP request operation.
            addrecords(tmpCON, re, rttime, entry[0])

        dbclose(tmpCR, tmpCON)
        sys.exit()

    sys.exit()


    # Three or more parameters passed.

if len(sys.argv) > 3:
    print('Way too many parameters, buddy.')
    sys.exit()

