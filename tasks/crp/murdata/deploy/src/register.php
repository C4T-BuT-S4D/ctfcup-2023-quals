<?php

require_once "DB.php";
require_once "session.php";

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    if (!isset($_POST['username']) || !isset($_POST['password']) || !isset($_POST['passport'])) {
        die("Missing username, password or passport");
    }

    $username = $_POST['username'];
    $password = $_POST["password"];
    $passport = $_POST["passport"];

    $db = new DB();

    if ($db->userExists($username)) {
        die("User already exists");
    }

    $userId = $db->addUser($username, $password, $passport);

    start_session($userId, $username);
    header("Location: /");
    return;
}

?>
<html>
<head>
    <title>MurSecrets - Register</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
<div class="main-block">
    <h2>Register</h2>
    <form method="post" action="">
        <label>
            Username:
            <input type="text" name="username" placeholder="Username">
        </label>
        <label>
            Password:
            <input type="password" name="password" placeholder="Password">
        </label>
        <label>
            Your passport id:
            <input type="text" name="passport" placeholder="1111 2222">
        </label>
        <input type="submit" value="Login">
    </form>

    <p>Already have an account? <a href="/login.php">Login</a></p>
</div>
</body>
</html>

