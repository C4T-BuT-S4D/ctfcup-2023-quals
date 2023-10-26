<?php

require_once "session.php";
require_once "DB.php";


$sess = get_session();
if (empty($sess)) {
    header("Location: /login.php");
    return;
}

$uid = $sess["userid"];
$username = $sess["username"];
$db = new DB();

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    if (array_key_exists("info", $_POST) === false || $_POST["info"] == "") {
        echo "Missing info.";
    } else {
        $db->setInfo($uid, $_POST["info"]);
    }
}

echo <<<HTML
<html lang="en">
<head>
    <title>MurSecrets - Login</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
<div class="main-block">
HTML;



$info = $db->getInfo($uid);

echo "<h3>Welcome ${username} ($uid)!<br></h3>";
echo "<h4>Your info: ${info}<br></h4>";
?>
<p>Update your information</p>
<form method="post" action="">
    <label>
        My information:
        <input type="text" name="info">
    </label>
    <input type="submit" name="Update">
</form>
<p>Check my <a href="/passport.php">passport id.</a></p>
</div>
</body>
</html>



