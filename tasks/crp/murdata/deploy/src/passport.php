<?php

require_once "session.php";
require_once "DB.php";

$sess = get_session();
if (empty($sess)) {
    header("Location: /login.php");
    return;
}

echo <<<HTML
<html lang="en">
<head>
    <title>MurSecrets - Login</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
HTML;


if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $uid = $sess["userid"];
    $username = $sess["username"];
    $db = new DB();

    if (array_key_exists("password", $_POST) === false || $_POST["password"] == "") {
        die("Missing password.");
    }

    if (!$db->isValidPassword($username, $_POST["password"])) {
        die("Invalid password.");
    }

    $passport = $db->getPassport($uid);
    echo "<h4>Your passport: ${passport}</h4><br>";
}
?>
<div class="main-block">
    <p>Please type your password again to access the passport information.</p>
    <form method="post" action="">
        <label>
            <input type="text" name="password">
        </label>
        <input type="submit" value="Get passport">
    </form>
</div>
</body>
</html>


