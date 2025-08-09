# JOURNALS 

# IMPLEMENTING THE API BACKEND ROUTES FOR JOURNALS 

# 1. GET only private journals for a current user (for a myPrivateJournals page)
@journals_routes.route('/private', methods=['GET']) # because this can only be retrieved once a journal entry exists, it will be in our journals.py file with prefix (api/journals/private)
@login_required                         # must be logged in and authorized 
def get_private_journals():   # we create a function called 'get_private_journals' that does not take in an id as an argument because we want to fetch all ids that are set to private 
    # so in order to fetch those private entries we need to scan our database and pull each journalId out that has the is_private column boolean set to true
    private_journals = Journal.query.filter_by(
        user_id
    ).all() # this variable will store the query that will "get all" journal.is_private entries from our Journal model

    # now that we have that variable set in place, we must check if the user logged in owns the journals 
    if private_journals.user_id != current_user.id: # so if the user_id foreign key in our journal table for those private_journals does not match the signed in user 
        return ({ "error": "Unauthorized"}), 403 # they do not have access to those private journals
    
    # if the above condition is false then that means the logged in user is the owner of those private_journals
    return (private_journals), 200 # return all private journal entries of the user 

# 2. POST a journal 


# 3. EDIT 
# 3a. PUT  /api/journals/:journalId (for this, let's say I have a list of journals in a speical div set up and display likes commments icons to the side of the div can i have a lock icon that taps into the is_private column for a quick change in the backend when using a thunk?)

# 3b. PATCH /api/journals/:journalId with { is_private: true/false } 
@journals_routes.route('/<int:journalId>', methods=['PATCH'])
@login_required
def toggle_journal_privacy(journalId): # we create a function by passing the journalId as an argument 
    journal = Journal.query.get(journalId) # we store that id in a variable to save it to use later 
    if not journal:                         # if that journal id does not exist we return our first obvious error 
        return ({"error": "Journal not found"}), 404
    
    # Only the owner can toggle privacy 
    if journal.user_id != current_user.id:  # now if the journal's user_id (our foreign key pointing to our users table) does not match the currently logged in user's id 
        return ({"error": "Unauthorized"}), 403     # return an unauthorized checkpoint meaning you can not make this change 
    
    data = request.get_json()                # we create a variable that stores the data into an object format of our journalId and all of it's components in key value pairs 
    if 'is_private' not in data:            # and if the key (aka column) is not discovered in our table 
        return ({ "error": "Missing 'is_private' field"}), 400  # we returrn another obvious error 
    
    is_private_value = data['is_private']      # if our is_private column exists, the entire object will be passed on to the data variable and we set another variable to store the [is_private value] by chaining it to data so it can tap into the key and extract that value
    if not isinstance(is_private_value, bool): # if the nature of the edit was not a boolean by some chance we would return a message 
        return ({ "error": "'is_private' must be a boolean"}), 400 # stating that it must be either trur or false (can't be a string, int, etc)
    
    journal.is_private = is_private_value       # if it is an instance of a boolean (either true or false) then we can continue to set our is_private column attached to that specific journalId to the is_private_value that has been altered in our frontend side
    db.session.commit() # whatever that change or selection was we commit that to the database (this is essentially the same logic for POST a journal and EDIT a journal minor difference being instead of going into one column we access and allow changes to all columns)

    return ({{                                  # the successful response after ensuring all those checks have been made would be the object response body to look like this    
        "id": journal.id,                       # the journalId that was of interest and authorization 
        "is_private": journal.is_private        # the altered stored value in the is_private column
    }}), 200                                    # with a success status (our thunk will play a role in dispatchign this without the hard refresh on the page)

# 4. DELETE a journal 
