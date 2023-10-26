<?php

function loadKey()
{
    return getenv('SESSION_SECRET') ?: "session_key";
}

function serializeArray($arr) {
    $str = "";
    foreach ($arr as $key => $value) {
        $str .= "${key}=${value}|";
    }
    return substr($str, 0, -1);
}

function unserializeArray($str) {
    $arr = [];
    $parts = explode("|", $str);
    foreach ($parts as $part) {
        $kv = explode("=", $part);
        if (count($kv) !== 2) {
            continue;
        }
        $arr[$kv[0]] = $kv[1];
    }
    return $arr;
}

function generateSession($userId, $username)
{
    $pld = serializeArray([
        "userid" => $userId,
        "username" => $username,
    ]);
    $key = loadKey();
    $hsh = hash('sha1', $key . "|" . $pld);
    $plde = base64_encode($pld);
    $hashe = base64_encode($hsh);
    return "${plde}.${hashe}";
}

function parseSession($session)
{
    $key = loadKey();
    $parts = explode(".", $session);
    if (count($parts) !== 2) {
        return null;
    }

    $pld = base64_decode($parts[0]);
    $hsh = base64_decode($parts[1]);
    $hsh2 = hash('sha1', $key . "|" . $pld);
    if ($hsh !== $hsh2) {
        return null;
    }

    return unserializeArray($pld);
}

function start_session($userId, $username)
{
    setcookie("mursession", generateSession($userId, $username));
}

function get_session() {
    if (!array_key_exists("mursession", $_COOKIE)) {
        return null;
    }

    return parseSession($_COOKIE["mursession"]);
}