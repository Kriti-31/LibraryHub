// Function to dynamically change user data on the dashboard
function updateUserInfo() {
    const userName = "John Doe"; // You can dynamically change this from a database/API
    const lastLogin = "2 hours ago"; // Dynamic data
    const profileInfo = "You have 5 unread messages"; // Dynamic info from the user profile
    const recentActivity = "You last updated your password yesterday"; // Dynamic recent activity
    const settingsStatus = "Your account is fully secure"; // Dynamic settings status

    // Updating the user name and last login time
    document.getElementById('userName').textContent = userName;
    document.getElementById('lastLogin').textContent = lastLogin;

    // Updating the profile, activity, and settings information
    document.getElementById('profileInfo').textContent = profileInfo;
    document.getElementById('recentActivity').textContent = recentActivity;
    document.getElementById('settingsStatus').textContent = settingsStatus;
}

// Call the function to update user info when the page loads
updateUserInfo();