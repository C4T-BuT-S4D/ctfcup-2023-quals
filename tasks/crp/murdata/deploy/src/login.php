<?php

require_once "DB.php";
require_once "session.php";

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    if (!isset($_POST['username']) || !isset($_POST['password'])) {
        die("Missing username, password");
    }

    $username = $_POST['username'];
    $password = $_POST["password"];

    $db = new DB();

    if (!$db->userExists($username)) {
        die("User does not exists.");
    }

    if (!$db->isValidPassword($username, $password)) {
        die("Invalid password.");
    }

    $uid = $db->getUserId($username);

    start_session($uid, $username);
    header("Location: /");
    return;
}

?>
<html>
<head>
    <title>MurSecrets - Login</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
<div class="main-block">
    <h2>Login</h2>
    <form method="post" action="">
        <input type="text" name="username" placeholder="Username">
        <input type="password" name="password" placeholder="Password">
        <input type="submit" value="Login">
    </form>

    <p>No account yet? <a href="/register.php">Register!</a></p>
</div>
</body>
</html>

