# GUI Architecture

## Application

The `Application` class:

- manages the Tk root window
- controls frame switching
- starts the application

## Frames

The GUI screens are implemented as subclasses of `tk.Frame`.

### 1. WelcomeFrame
- Initial screen
- Offers navigation to Sign Up or Sign In

### 2. SignUpFrame
- Accepts username and password
- Stores user credentials locally

### 3. SignInFrame
- Validates credentials
- Redirects authenticated user to `MainFrame`

### 4. MainFrame
- Main dashboard of the application
- Displays quick account statistics
- Provides navigation to input and inspection views

### 5. InputFrame
- Used to create new revenues, expenses, obligations, or wishlist items

### 6. InspectFrame
- Displays existing entries
- Supports export to Excel