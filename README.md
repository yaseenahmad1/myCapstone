# myCapstone

DEMONSTRATION 
5 users 
1. gold tree
2. 4/5 gold tree
3. 3/5 gold  tree
4. 2/5 gold tree
5. 0/5 gold tree

PLAN : Create gallery and journal page fully save comments, likes and follows till end focus on hoempage and these two feature 

You don’t need to change the reducer for a redirect — the reducer’s job is just to update the Redux state. Right now, your CREATE_GALLERY case already adds the new gallery into currentUserGalleries, so the state is correct and has all the info you need (including its id). ✅

Redirecting to the single gallery page is purely a frontend/React thing. For example, after dispatching the thunkCreateGallery in your component, you can use React Router’s useNavigate to go to the new gallery’s page:

const navigate = useNavigate();

const handleSubmit = async (gallery) => {
  const newGallery = await dispatch(thunkCreateGallery(gallery));
  if (newGallery && newGallery.id) {
    navigate(`/galleries/${newGallery.id}`);
  }
};

# your tree progree bar logic : 
```js
 const updateTreeProgress = (galleryId, journalId) => {
     // idea is to create a function that whenever a new gallery or journal is added or if one or the other is deleted we update the tree bar status based on total_progress column of our users object 
     galleryNumAltered = galleryId
     // use a dispatch that fetches user information whenever

//Returning data from your thunk allows any component or function that calls the thunk to immediately use the fetched gallery, without waiting for Redux state to update.

//For example:

const handleGalleryClick = async (galleryId) => {
  const gallery = await dispatch(thunkGetGallery(galleryId));
  console.log(gallery); // you have the full gallery object right away
  updateTreeProgress(gallery); // you can use it to update progress bar immediately
};


//Without return data, the component would have to rely on the Redux state after it updates, which can sometimes require extra useEffect hooks.

//Returning it makes your thunks more flexible — you can use them both to update state and get immediate access to data for side effects (like updating a progress tree).

//So yes, for your tree progress bar feature, returning the data from the thunk is actually really useful.

//If you want, I can show a pattern for all your gallery thunks with this “return data” approach, so your frontend logic will be ready for things like the progress tree.
```

# FRONTEND GAME PLAN 

Sunday - Worked on greeting page, home page, set up thunks and reducers
Sunday - set up my store by creating all the action types, action creators, thunks and reducers that I will need 
Monday - set up all create form pages (Gallery Form page, Journal Form Page, Comment Form Page) --- if i have time create the Edit form pages for them (same thing just use PUT thunks to auto fill form)
Tuesday - set up layout for how galleries and journal entries within a gallery will look on a user's profile and Create tree black to gold 10 grid rows connected to total progress of a user,
Wednesday - Add the screensave welcome page we did and the sprial image for our landing page
Thursday - 

# Features List 

```js
1. myJournalGallery
     - Users should be able to get all journalGalleries they own
     - User can create a myjournalGallery that stores relevant journal entries
     - Users can edit that journalGallery (image, title, chapter#:verse#, description)
     - Users can delete the journalGallery and all of it's related journals in one click 
3. myReflectionJournal
     - Users should be able to get all journal entries they own
     - Users can add a journal entry in their journal gallery
     - Users can make edits to that entry by changing the title, image, chapter#:verse#, text_body
     - Users can delete a single journal entry 
5. myConnections
     - Users should be able to view all of their connections (who they follow and who follows them)
     - Users should be able to follow another user
     - Users should be able to unfollow another user 
7. Comments
     - Users should be able to view all comments under a journalGallery
     - Users should be able to add a comment under another user's journalGallery
     - Users should be able to edit their existing comment
     - Users should be able to delete their exisiting comment 
9. Likes
     - Users should be able to view all likes on an existing journalGallery or reflectionJournal
     - Users should be able to like a journalGallery or a specific journal post
     - Users should be able to remove a like from a journalGallery or a specific journal post
```

# DB Schema 

```js
[Please refer to image inside this repo]

TABLE RELATIONSHIPS

1. A user can have many journalGalleries
2. A user can have many journalEntries
3. A user can have many followers
4. Many users can follow a user 
5. A journalGallery can have many journalEntries
6. Many journalEntries belong to one journalGallery
7. A journalGallery can have many comments
8. A journalGallery can have many likes
9. A journalEntry can have many likes
```

# USERS 

```python
class User(db.Model, UserMixin):
    __tablename__ = 'users'

    if environment == "production":
        __table_args__ = {'schema': SCHEMA}

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), nullable=False, unique=True)
     # field required
    email = db.Column(db.String(255), nullable=False, unique=True)
     # field required
    first_name = db.Column(db.String(40), nullable=False)
     # field required
    last_name = db.Column(db.String(40), nullable=False)
     # field required
    hashed_password = db.Column(db.String(255), nullable=False)
     # field required

    # Relationships
    likes = db.relationship("Like", back_populates="user", cascade="all, delete-orphan")  
    # A user can give many likes, deleting user removes their likes

    following = db.relationship("Follow", foreign_keys=[Follow.follower_id], back_populates="follower", cascade="all, delete-orphan")  
    # All follow relationships where this user is the one doing the following

    followers = db.relationship("Follow", foreign_keys=[Follow.following_id], back_populates="following", cascade="all, delete-orphan")  
    # All follow relationships where this user is being followed

    comments = db.relationship("Comment", back_populates="user", cascade="all, delete-orphan")  
    # A user can leave many comments, deleting user removes their comments

    journals = db.relationship("Journal", back_populates="user", cascade="all, delete-orphan")  
    # A user can have many journals, deleting user removes their journals

    galleries = db.relationship("Gallery", back_populates="user", cascade="all, delete-orphan")  
    # A user can have many galleries, deleting user removes their galleries
```

# FOLLOWS

```python
class Follow(db.Model, TimeStampMixin):
    __tablename__ = "follows"

    if environment == "production":
        __table_args__ = {"schema": SCHEMA}

    id = db.Column(db.Integer, primary_key=True)
    follower_id = db.Column(db.Integer, db.ForeignKey(add_prefix_for_prod("users.id")), nullable=False)
    following_id = db.Column(db.Integer, db.ForeignKey(add_prefix_for_prod("users.id")), nullable=False)

    # Relationships
    follower = db.relationship("User", foreign_keys=[follower_id], back_populates="following")  
    # The user who is following someone

    following = db.relationship("User", foreign_keys=[following_id], back_populates="followers")  
    # The user who is being followed
```

# GALLERIES 

```python
class Gallery(db.Model, TimeStampMixin):
    __tablename__ = 'galleries'

    if environment == "production":
        __table_args__ = {'schema': SCHEMA}

    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String(255), nullable=False)
     # field required
    title = db.Column(db.String(250), nullable=False)
     # field required
    surah = db.Column(db.Integer, nullable=True)
     # field not required
    verse = db.Column(db.Integer, nullable=True)
     # field not required
    arabic_text = db.Column(db.String, nullable=True)
     # field not required
    english_text = db.Column(db.String, nullable=True)
     # field not required
    description = db.Column(db.String(), nullable=False)
     # field required
    user_id = db.Column(db.Integer, db.ForeignKey(add_prefix_for_prod("users.id")))

    # Relationships
    user = db.relationship("User", back_populates="galleries")  
    # A gallery belongs to a single user

    journals = db.relationship("Journal", back_populates="gallery", cascade="all, delete-orphan")  
    # A gallery can have many journals, deleting gallery removes its journals
```

# JOURNALS 

```python
class Journal(db.Model, TimeStampMixin):
    __tablename__ = 'journals'

    if environment == "production":
        __table_args__ = {'schema': SCHEMA}

    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String(255), nullable=False)
     # field required
    title = db.Column(db.String(250), nullable=False)
     # field required
    surah = db.Column(db.Integer, nullable=False)
     # field required
    verse = db.Column(db.Integer, nullable=False)
     # field required
    arabic_text = db.Column(db.String, nullable=False)
     # field required
    english_text = db.Column(db.String, nullable=False)
     # field required
    description = db.Column(db.String(), nullable=False)
     # field required
    is_private = db.Column(db.Boolean(), nullable=False, default=False)
     # Privacy flag for journal
    user_id = db.Column(db.Integer, db.ForeignKey(add_prefix_for_prod("users.id")))
     # for fetching and cascade delete purposes so if a user is deleted all journal entries connected to that user will be deleted as well 
    gallery_id = db.Column(db.Integer, db.ForeignKey(add_prefix_for_prod("galleries.id")))
     # for fetching and cascade delete purposes so if a gallery is deleted all journal entries connected to that gallery will be deleted as well 


    # Relationships
    user = db.relationship("User", back_populates="journals")  
    # A journal belongs to one user

    comments = db.relationship("Comment", back_populates="journal", cascade="all, delete-orphan")  
    # A journal can have many comments, deleting journal removes them

    likes = db.relationship("Like", back_populates="journal", cascade="all, delete-orphan")  
    # A journal can have many likes, deleting journal removes them

    gallery = db.relationship("Gallery", back_populates="journals")  
    # A journal belongs to one gallery
```

# COMMENTS 

```python
class Comment(db.Model, TimeStampMixin):
    __tablename__ = 'comments'

    if environment == 'production':
        __table_args__ = {'schema': SCHEMA}
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(add_prefix_for_prod("users.id")), nullable=False)
    journal_id = db.Column(db.Integer, db.ForeignKey(add_prefix_for_prod("journals.id")), nullable=False)
    comment_body = db.Column(db.String(300), nullable=False)
     # field required

    # Relationships
    user = db.relationship("User", back_populates="comments")  
    # A comment belongs to one user

    journal = db.relationship("Journal", back_populates="comments")  
    # A comment belongs to one journal
```

# LIKES 

```python
class Like(db.Model):
    __tablename__ = 'likes'

    if environment == 'production':
        __table_args__ = {'schema': SCHEMA}

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(add_prefix_for_prod("users.id")), nullable=False)
    journal_id = db.Column(db.Integer, db.ForeignKey(add_prefix_for_prod("journals.id")), nullable=False)

    # Relationships
    user = db.relationship("User", back_populates="likes")  
    # A like belongs to one user

    journal = db.relationship("Journal", back_populates="likes")  
    # A like belongs to one journal
```

# Backend API Routes

# `myIslamTree`

## Database Schema Design

`<insert database schema design here>`

## API Documentation

## USER AUTHENTICATION/AUTHORIZATION

### All endpoints that require authentication

All endpoints that require a current user to be logged in.

* Request: endpoints that require authentication
* Error Response: Require authentication
  * Status Code: 401
  * Headers:
    * Content-Type: application/json
  * Body:

    ```json
    {
      "message": "Authentication required"
    }
    ```

### All endpoints that require proper authorization

All endpoints that require authentication and the current user does not have the
correct role(s) or permission(s).

* Request: endpoints that require proper authorization
* Error Response: Require proper authorization
  * Status Code: 403
  * Headers:
    * Content-Type: application/json
  * Body:

    ```json
    {
      "message": "Forbidden"
    }
    ```

### Get the Current User

Returns the information about the current user that is logged in.

* Require Authentication: true
* Request
  * Method: GET
  * Route path: /api/users/:userId
  * Body: none

* Successful Response when there is a logged in user
  * Status Code: 200
  * Headers:
    * Content-Type: application/json
  * Body:

    ```json
    {
      "user": {
        "id": 1,
        "firstName": "John",
        "lastName": "Smith",
        "email": "john.smith@gmail.com",
        "username": "JohnSmith"
      }
    }
    ```

* Successful Response when there is no logged in user
  * Status Code: 200
  * Headers:
    * Content-Type: application/json
  * Body:

    ```json
    {
      "user": null
    }
    ```

### Log In a User

Logs in a current user with valid credentials and returns the current user's
information.

* Require Authentication: false
* Request
  * Method: POST
  * Route path: api/users/:userId
  * Headers:
    * Content-Type: application/json
  * Body:

    ```json
    {
      "credential": "john.smith@gmail.com",
      "password": "secret password"
    }
    ```

* Successful Response
  * Status Code: 200
  * Headers:
    * Content-Type: application/json
  * Body:

    ```json
    {
      "user": {
        "id": 1,
        "firstName": "John",
        "lastName": "Smith",
        "email": "john.smith@gmail.com",
        "username": "JohnSmith"
      }
    }
    ```

* Error Response: Invalid credentials
  * Status Code: 401
  * Headers:
    * Content-Type: application/json
  * Body:

    ```json
    {
      "message": "Invalid credentials"
    }
    ```

* Error response: Body validation errors
  * Status Code: 400
  * Headers:
    * Content-Type: application/json
  * Body:

    ```json
    {
      "message": "Bad Request", // (or "Validation error" if generated by Sequelize),
      "errors": {
        "credential": "Email or username is required",
        "password": "Password is required"
      }
    }
    ```

### Sign Up a User

Creates a new user, logs them in as the current user, and returns the current
user's information.

* Require Authentication: false
* Request
  * Method: POST
  * Route path: /api/session
  * Headers:
    * Content-Type: application/json
  * Body:

    ```json
    {
      "firstName": "John",
      "lastName": "Smith",
      "email": "john.smith@gmail.com",
      "username": "JohnSmith",
      "password": "secret password"
    }
    ```

* Successful Response
  * Status Code: 201
  * Headers:
    * Content-Type: application/json
  * Body:

    ```json
    {
      "user": {
        "id": 1,
        "firstName": "John",
        "lastName": "Smith",
        "email": "john.smith@gmail.com",
        "username": "JohnSmith"
      }
    }
    ```

* Error response: User already exists with the specified email or username
  * Status Code: 500
  * Headers:
    * Content-Type: application/json
  * Body:

    ```json
    {
      "message": "User already exists",
      "errors": {
        "email": "User with that email already exists",
        "username": "User with that username already exists"
      }
    }
    ```

* Error response: Body validation errors
  * Status Code: 400
  * Headers:
    * Content-Type: application/json
  * Body:

    ```json
    {
      "message": "Bad Request", // (or "Validation error" if generated by Sequelize),
      "errors": {
        "email": "Invalid email",
        "username": "Username is required",
        "firstName": "First Name is required",
        "lastName": "Last Name is required"
      }
    }
    ```

## myJournalGallery

### Get all the galleries owned by current user 

Returns all the journalGalleries of current user.

* Require Authentication: true 
* Request
  * Method: GET
  * Route path: /api/galleries/current
  * Body: none

* Successful Response
  * Status Code: 200
  * Headers:
    * Content-Type: application/json
  * Body:

    ```json
    {
      "galleries": [
        {
          "id": 1,
          "userId": 1,
          "image" : "image url", 
          "title": "Celestial Objects",
          "surah_number": 17,
          "verse_number": 12,
          "arabic_text": "arabic text",           
          "english_text": "english translation",
          "description": "body text",
          "createdAt": "2025-7-19 20:39:36",
          "updatedAt": "2025-7-19 20:39:36",
          "numOfJournalEntries": 3, 
          "numOfLikes": 14,
          "numOfComments": 10
        },
        {
          "id": 2,
          "userId": 1,
          "image" : "image url", 
          "title": "Winds",
          "surah_number": 7,
          "verse_number": 57,
          "arabic_text": "arabic text",           
          "english_text": " english translation",
          "createdAt": "2025-7-19 20:39:36",
          "updatedAt": "2025-7-19 20:39:36",
          "numOfJournalEntries": 5, 
          "numOfLikes": 10,
          "numOfComments": 2
        },
      ]
    }
    ```

### Create a `Gallery`

Creates and returns a new gallery.

* Require Authentication: true
* Request
  * Method: POST
  * Route path: /api/galleries/create
  * Headers:
    * Content-Type: application/json
  * Body:

    ```json
    {
    "image" : "image url", 
    "title": "Opening",
    "surah_number": 1,
    "verse_number": 1,
    "description": "body text",
    }
    ```

* Successful Response
  * Status Code: 201
  * Headers:
    * Content-Type: application/json
  * Body:

    ```json
        {
          "id": 3,
          "userId": 1,
          "image" : "image url", 
          "title": "Opening",
          "surah_number": 1,
          "verse_number": 1,
          "arabic_text": "arabic text",           
          "english_text": "english translation",
          "description": "body text",
          "createdAt": "2025-7-19 20:39:36",
          "updatedAt": "2025-7-19 20:39:36",
          "numOfJournalEntries": 0, 
          "numOfLikes": 0,
          "numOfComments": 0 
        } 
    ```

* Error Response: Body validation errors
  * Status Code: 400
  * Headers:
    * Content-Type: application/json
  * Body:

    ```json
    {
      "message": "Bad Request", 
      "errors": 
      { 
        "image": "Image must be a jpeg, pdf, or url",
        "title": "Title is required.",
        "surah_number": optional,
        "verse_number": optional,
        "arabic_text": "arabic text", optional          
        "english_text": "english translation", optional
        "description": "Description is required",
      }
    }
    ```

### Edit a `Gallery`/Add an Image to a `Gallery`

Updates and returns an existing gallery.

* Require Authentication: true
* Require proper authorization: Gallery must belong to the current user
* Request
  * Method: PUT
  * Route path: /api/galleries/:galleryId
  * Headers:
    * Content-Type: application/json
  * Body:

    ```json
    {
    "image" : "image url", 
    "title": "Opening",
    "surah_number": 1,
    "verse_number": 4,                      # edit made 
    "description": "new body text",         # edit made 
    }
    ```

* Successful Response
  * Status Code: 200
  * Headers:
    * Content-Type: application/json
  * Body:

    ```json
    {
          "id": 3,
          "userId": 1,
          "image" : "image url", 
          "title": "Opening",
          "surah_number": 1,
          "verse_number": 4,                # change reflected
          "arabic_text": "arabic text",           # change reflected
          "english_text": "english translation",  # change reflected
          "description": "new body text",         # change reflected 
          "createdAt": "2025-7-19 20:39:36",
          "updatedAt": "2025-7-19 20:39:36",
          "numOfJournalEntries": 0, 
          "numOfLikes": 0,
          "numOfComments": 0 
        } 
    ```

* Error Response: Body validation errors
  * Status Code: 400
  * Headers:
    * Content-Type: application/json
  * Body:

    ```json
    {
      "message": "Oops! Something went wrong", 
      "errors": 
      {
        "image": "Image must be a jpeg, pdf, or url",
        "title": "Title is required.",
        "surah_number": optional,
        "verse_number": optional,
        "arabic_text": "arabic text", optional          
        "english_text": "english translation", optional
        "description": "Description is required",
      }
    }
    ```

* Error response: Couldn't find a Gallery with the specified id
  * Status Code: 404
  * Headers:
    * Content-Type: application/json
  * Body:

    ```json
    {
      "message": "This gallery most probably does not exist"
    }
    ```

### Delete a `Gallery`

Deletes an existing gallery.

* Require Authentication: true
* Require proper authorization: Gallery must belong to the current user
* Request
  * Method: DELETE
  * Route path: /api/galleries/:galleryId
  * Body: none

* Successful Response
  * Status Code: 200
  * Headers:
    * Content-Type: application/json
  * Body:

    ```json
    {
      "message": "Your gallery and associated journal entries have been successfully deleted"
    }
    ```

* Error response: Couldn't find a gallery with the specified id
  * Status Code: 404
  * Headers:
    * Content-Type: application/json
  * Body:

    ```json
    {
      "message": "Hmmm... that gallery couldn't be found"
    }
    ```
## myReflectionJournal

### Get all the journals of a gallery

Returns all the journal entries of a journalGallery. 

* Require Authentication: true 
* Request
  * Method: GET
  * Route path: /api/galleries/:galleryId/journals
  * Body: none

* Successful Response
  * Status Code: 200
  * Headers:
    * Content-Type: application/json
  * Body:

    ```json
    {
      "galleryId": 1,
      "userId": 1, 
      "journals" : [
         {
              "id": 1,                                                              
              "image" : "image url", 
              "title": "The Moon",
              "surah_number": 17,
              "verse_number": 12,
              "arabic_text": "arabic text",           
              "english_text": "english translation",
              "journal_entry": "body text",
              "createdAt": "2025-7-19 20:39:36",
              "updatedAt": "2025-7-19 20:39:36", 
              "numOfLikes": 14,
         },
         {
              "id": 2,                            
              "image" : "image url", 
              "title": "The Sun",
              "surah_number": 7,
              "verse_number": 57,
              "arabic_text": "arabic text",           
              "english_text": " english translation",
              "createdAt": "2025-7-19 20:39:36",
              "updatedAt": "2025-7-19 20:39:36",
              "numOfLikes": 10,
          },
         ]
    }
    ```

### Get all the journals of the current user 

Returns all the journal entries ever made by the logged in user. 

* Require Authentication: true 
* Request
  * Method: GET
  * Route path: /api/journals  # fetches all existing journal entries so this will be in our journals.py route file 
  * Body: none

* Successful Response
  * Status Code: 200
  * Headers:
    * Content-Type: application/json
  * Body:

    ```json
    {
    
         "journals" : [
               {
                   "id": 1,
                   "userId" : 1,
                   "galleryId": 1, # do we need the gallery id associated with the journal entry? (perhaps if i want to click on that tile and it takes me to the full gallery page)                                                           
                   "image" : "image url", 
                   "title": "The Moon",
                   "surah_number": 17,
                   "verse_number": 12,
                   "arabic_text": "arabic text",           
                   "english_text": "english translation",
                   "journal_entry": "body text",
                   "createdAt": "2025-7-19 20:39:36",
                   "updatedAt": "2025-7-19 20:39:36", 
                   "numOfLikes": 14,
               },
               {
                   "id": 2,
                   "userId": 2,
                   "galleryId": 1,                         
                   "image" : "image url",
                   "title": "The Sun",
                   "surah_number": 7,
                   "verse_number": 57,
                   "arabic_text": "arabic text",           
                   "english_text": "english translation",
                   "journal_entry": "body text", 
                   "createdAt": "2025-7-19 20:39:36",
                   "updatedAt": "2025-7-19 20:39:36",
                   "numOfLikes": 10,
               },
         ]
    }
    ```
    
### Create a `Journal`

Creates and returns a new journal.

* Require Authentication: true
* Request
  * Method: POST
  * Route path: /api/galleries/:galleryId/journals     # this route will be in our galleries.py route file because the only way to write a journal entry is within an existing gallery
  * Headers:
    * Content-Type: application/json
  * Body:

    ```json
    {
    "image" : "image url",
    "title": "Adam",
    "surah_number": 2,
    "verse_number": 1,
    "journal_entry": "body text",
    }
    ```

* Successful Response
  * Status Code: 201
  * Headers:
    * Content-Type: application/json
  * Body:

    ```json
        {
          "id": 3,               # new id number generated upon creation 
          "userId": 1,
          "galleryId": 1, 
          "image" : "image url",
          "title": "Adam",
          "surah_number": 2,
          "verse_number": 1,
          "arabic_text": "arabic text",           
          "english_text": "english translation",
          "journal_entry": "body text",
          "createdAt": "2025-7-19 20:39:36",
          "updatedAt": "2025-7-19 20:39:36",
          "numOfLikes": 0,
        } 
    ```

* Error Response: Body validation errors
  * Status Code: 400
  * Headers:
    * Content-Type: application/json
  * Body:

    ```json
    {
      "message": "Bad Request", 
      "errors": 
      { 
        "image": "Image must be a jpeg, pdf, or url",
        "title": allowNull,
        "surah_number": surah number is required,
        "verse_number": surah number is required,
        "arabic_text": "arabic text",           
        "english_text": "english translation", 
        "journal_entry": "This field cannot be empty",
      }
    }
    ```

### Edit a `Journal`

Updates and returns an existing journal.

* Require Authentication: true
* Require proper authorization: Journal must belong to the current user
* Request
  * Method: PUT
  * Route path: /api/journals/:journalId    # now that our journal id exists, this route will be coded in our journals.py file 
  * Headers:
    * Content-Type: application/json
  * Body:

    ```json
    {
    "image" : "image url",
    "title": "The Creation of Man",           # edit made here
    "surah_number": 2,
    "verse_number": 10,                       # edit made here
    "journal_entry": "body text",
    }
    ```

* Successful Response
  * Status Code: 200
  * Headers:
    * Content-Type: application/json
  * Body:

    ```json
    {
          "id": 3,                         # same id number 
          "userId": 1,
          "galleryId": 1, 
          "image" : "image url",
          "title": "The Creation of Man",     # changed field 
          "surah_number": 2,
          "verse_number": 10,                 # changed field 
          "arabic_text": "arabic text",       # changed verse 
          "english_text": "english translation", # changed verse 
          "journal_entry": "body text",
          "createdAt": "2025-7-19 20:39:36",
          "updatedAt": "2025-7-19 20:39:36",
          "numOfLikes": 0,
        } 
    ```

* Error Response: Body validation errors
  * Status Code: 400
  * Headers:
    * Content-Type: application/json
  * Body:

    ```json
    {
      "message": "Oops! Something went wrong", 
      "errors": 
      {
        "image": "Image must be a jpeg, pdf, or url",
        "title": "Title is required.",
        "surah_number": "this field is required",
        "verse_number": "this field is required",
        "arabic_text": "arabic text", required          
        "english_text": "english translation", required
        "description": "Description is required",
      }
    }
    ```

* Error response: Couldn't find a journal with the specified id
  * Status Code: 404
  * Headers:
    * Content-Type: application/json
  * Body:

    ```json
    {
      "message": "This journal most probably does not exist"
    }
    ```

### Delete a `Journal`

Deletes an existing journal.

* Require Authentication: true
* Require proper authorization: Journal must belong to the current user
* Request
  * Method: DELETE
  * Route path: /api/journals/:journalId      # same route as edit but our method is DELETE now so this will occur in our journals.py file 
  * Body: none

* Successful Response
  * Status Code: 200
  * Headers:
    * Content-Type: application/json
  * Body:

    ```json
    {
      "message": "Your journal has been successfully deleted"
    }
    ```

* Error response: Couldn't find a post with the specified id
  * Status Code: 404
  * Headers:
    * Content-Type: application/json
  * Body:

    ```json
    {
      "message": "Hmmm... that journal couldn't be found"
    }
    ```

## COMMENTS

### Get all `COMMENTS` of the Current Gallery by `galleryId`

Returns all the comments of the current Gallery. (Lazy or Eager Loading) (Possible pagination: 10 comments at a time)

* Require Authentication: true
* Request
  * Method: GET 
  * Route path: /api/galleries/:galleryId/comments?page=1&limit=10          # we will place this path in our galleries file where that is the place to retrieve comments attached to a particular gallery - adding query params for pagination if                                                                                       comments exceed 10 
  * Body: none

* Successful Response
  * Status Code: 200
  * Headers:
    * Content-Type: application/json
  * Body:

    ```json
    {
      "Comments": [
        {
          "id": 1,
          "userId": 1,
          "galleryId": 1,
          "comment": "Hey! I'm so glad you made an account!",
          "createdAt": "2021-11-19 20:39:36",
          "updatedAt": "2021-11-19 20:39:36",
          "User":
             {
                 "id": 1,
                 "userName": "yaya30"
             },
        },
        {
          // more comments 
        }
      ],
     "page": 1,
     "totalPages": 5
    }

    
    ```

### Create a Comment for a `Gallery` based on the `galleryId`

Create and return a new comment for a gallery specified by its id.

* Require Authentication: true
* Request
  * Method: POST
  * Route path: /api/galleries/:galleryId/comments          # since we are creating a new comment, this will be placed in our galleries.py routes file 
  * Headers:
    * Content-Type: application/json
  * Body:

    ```json
    {
      "comment": "Cool post!",
    }
    ```

* Successful Response
  * Status Code: 201
  * Headers:
    * Content-Type: application/json
  * Body:

    ```json
    {
      "id": 1,
      "userId": 1,
      "galleryId": 1,
      "comment": "Cool post!",
      "createdAt": "2021-11-19 20:39:36",
      "updatedAt": "2021-11-19 20:39:36"
    }
    ```

* Error Response: Body validation errors
  * Status Code: 400
  * Headers:
    * Content-Type: application/json
  * Body:

    ```json
    {
      "message": "Bad Request", 
      "errors": 
    {
      "comment": "Text is required to post a comment"
    }
    }
    ```

* Error response: Couldn't find a Gallery with the specified id
  * Status Code: 404
  * Headers:
    * Content-Type: application/json
  * Body:

    ```json
    {
      "message": "Gallery couldn't be found"
    }
    ```

### Edit a Comment

Update and return an existing comment.

* Require Authentication: true
* Require proper authorization: Comment must belong to the current user
* Request
  * Method: PUT
  * Route path: /api/comments/:commentId           # now that our comment exists this code will be handled in comments.py file 
  * Headers:
    * Content-Type: application/json
  * Body:

    ```json
    {
      "comment": "This was an awesome post!"
    }
    ```

* Successful Response
  * Status Code: 200
  * Headers:
    * Content-Type: application/json
  * Body:

    ```json
    {
      "id": 1,
      "userId": 1,
      "galleryId": 1,
      "comment": "This was an awesome post!",
      "createdAt": "2021-11-19 20:39:36",
      "updatedAt": "2021-11-20 10:06:40"
    }
    ```

* Error Response: Body validation errors
  * Status Code: 400
  * Headers:
    * Content-Type: application/json
  * Body:

    ```json
    {
      "message": "Bad Request", 
      "errors": 
      {
        "comment": "Text is required",
      }
    }
    ```

### Delete a Comment

Delete an existing comment.

* Require Authentication: true
* Require proper authorization: Comment must belong to the current user
* Request
  * Method: DELETE
  * Route path: /api/comments/:commentId                # same route different method in comments.py file 
  * Body: none

* Successful Response
  * Status Code: 200
  * Headers:
    * Content-Type: application/json
  * Body:

    ```json
    {
      "message": "This comment has been successfully deleted"
    }
    ```

## LIKES

### View/Get all of the Current Gallery `LIKES`

Return all the likes [`and the usernames associated with those likes`] that the current post has.

* Require Authentication: true
* Request
  * Method: GET
  * Route path: api/galleries/:galleryId/likes           # this will be placed in our galleries.py file where we can tap into a specific gallery and extract all users who liked the gallery
  * Body: none

* Successful Response
  * Status Code: 200
  * Headers:
    * Content-Type: application/json
  * Body:

    ```json
    {
    "gallery": 
        {
            "galleryId": 1,
            "numOfLikes": 3, // Response would show a total number of likes that a post has that increments and decrements w/o hard refresh
            "likedByCurrentUser": true, 
            "likedUsers": [
                    // Upon clicking on "Likes" for a post a drop down or modal of userNames appears to the logged in user
                    { "id":1, "userName": "JSmith30"},
                    { "id":2, "userName": "PokemonMaster21"},
                    { "id":3, "userName": "Demo-lition"}
            ]
        },
    }
    ```

### Add a `LIKE` to a `Gallery` based on the `galleryId` 

Add a like to a gallery based on the galleryId.

* Require Authentication: true
* Require proper authorization: n/a (postId must exist)
* Request
  * Method: POST 
  * Route path: api/galleries/:galleryId/likes          # this will add a like to a specific gallery 
  * Headers:
    * Content-Type: application/json
  * Body: None 


* Successful Response
  * Status Code: 201
  * Headers:
    * Content-Type: application/json
  * Body:

    ```json
    {
      "likeId": 1, // will a like have a "likeId" column? 
      "galleryId": 1,
      "userId": 2,
      "createdAt": "2021-11-19 20:39:36",
      "updatedAt": "2021-11-19 20:39:36"
    }
    ```
* will we build the like table to have a likeId column that has true and false or 1 and 0 so if a post is liked that will assign a likeId which will connect a user and a like together?

* Error response: Body validation errors
  * Status Code: 400
  * Headers:
    * Content-Type: application/json
  
  `post can only be liked or unliked so no error response for this feature`

### Remove a `LIKE` from a `Gallery` based on the `galleryId` 

Remove a like to a post based on the postId.

* Require Authentication: true
* Require proper authorization: n/a (postId must exist)
* Request
  * Method: DELETE
  * Route path: /api/galleries/:galleryId/likes           # I chose to keep this in the same file because the other two require it and I feel like it is simpler to have all likes route in one place rather than one outside of the other two
  * Headers:
    * Content-Type: application/json
  * Body: None

* Successful Response
  * Status Code: 201
  * Headers:
    * Content-Type: application/json
  * Body:

    ```json
    {
      "likeId": 1, // will a like have a "likeId" column? 
      "galleryId": 1,
      "userId": 2,
      "deletedAt": "2021-11-19 20:39:36"
    }

## FOLLOWS          

### View/Get all of the Current User's `FOLLOWING LIST`

Return a list of the users that the current user follows. 

* Require Authentication: true
* Request
  * Method: GET
  * Route path: api/users/:userId/following               # this will be in our users.py where we will be able to see the users that the current user is following 
  * Body: none

* Successful Response
  * Status Code: 200
  * Headers:
    * Content-Type: application/json
  * Body:

    ```json
    {
         "userId": 1,
         "following": [
              { "id": 2, "userName": "JSmith30" },
              { "id": 3, "userName": "PokemonMaster21" },
              { "id": 4, "userName": "Demo-lition" }
            ]
     }

    ```
### View/Get all of the Current User's `FOLLOWERS LIST`

Return a list of the users that follow the current user.

* Require Authentication: true
* Request
  * Method: GET
  * Route path: api/users/:userId/followers               # this will be in our users.py where we will be able to see the people who follow the current user 
  * Body: none

* Successful Response
  * Status Code: 200
  * Headers:
    * Content-Type: application/json
  * Body:

    ```json
         {
           "userId": 1,
           "followers": [
              { "id": 5, "userName": "User5" },
              { "id": 6, "userName": "User6" }
            ]
         }

    ```

### Add a `FOLLOW` to a `USER` based on the `userId` 

Add a "follow" to a user's profile based on a `user's Id`.

* Require Authentication: true
* Require proper authorization: current user
* Request
  * Method: POST
  * Route path: /api/users/:userid/follow               # this will also exist in our users.py file 
  * Headers:
    * Content-Type: application/json
  * Body: None

* Successful Response
  * Status Code: 201
  * Headers:
    * Content-Type: application/json
  * Body:

    ```json
          {
            "followId": 1,
            "followerId": 3,     // current user (who is doing the following)
            "followingId": 1,    // the target user being followed
            "createdAt": "2025-08-06T16:00:00Z",
            "updatedAt": "2025-08-06T16:00:00Z"
          }

    ```
* will we build the like table to have a likeId column that has true and false or 1 and 0 so if a post is liked that will assign a likeId which will connect a user and a like together?

* Error response: Body validation errors
  * Status Code: 400
  * Headers:
    * Content-Type: application/json
  
  `post can only be liked or unliked so no error response for this feature`

### Remove a `FOLLOW` based on the `userId` - `DELETE` method - 

FOR LIKES AND FOLLOWS WE HAVE TO FIGURE OUT A WAY TO DO THIS WITHOUT USING POST AND DELETE METHODS (COULD BE FRONTEND BEHAVIOR)

Remove a follow from following list based on the userId.

* Require Authentication: true
* Require proper authorization: userId must exist
* Request
  * Method: DELETE
  * Route path: /api/users/:userId/unfollow               # we tap into the user we intend to unfollow? 
  * Headers:
    * Content-Type: application/json
  * Body: None

* Successful Response
  * Status Code: 201
  * Headers:
    * Content-Type: application/json
  * Body:

    ```json
          {
            "unfollowed": true,
            "followerId": 3,
            "unfollowedUserId": 1,
            "deletedAt": "2025-08-06T16:00:00Z"
          }

