<?php

class DB
{
    private $redis;
    public function __construct()
    {
        $this->redis = new Redis([
            'host' => getenv("REDIS_HOST") ?: "localhost",
            'port' => 6379,
            'connectTimeout' => 2.5,
            'backoff' => [
                'algorithm' => Redis::BACKOFF_ALGORITHM_DECORRELATED_JITTER,
                'base' => 500,
                'cap' => 750,
            ],
        ]);
    }

    public function userExists($username) {
        return $this->redis->hExists("users", $username);
    }

    public function getUserId($username) {
        return $this->redis->hGet("user_ids", $username);
    }

    private function hashPassword($password) {
        return hash('murmur3f', $password);
    }

    private function compareHashes($hash1, $hash2) {
        return hexdec($hash1) === hexdec($hash2);
    }

    public function addUser($username, $password, $passport) {
        $userId = $this->redis->incr("user_id");
        $this->redis->hSet("users", $username, $this->hashPassword($password));
        $this->redis->hSet("user_ids", $username, $userId);
        $this->redis->hSet("user_passports", $userId, $passport);
        return $userId;
    }

    public function getPassport($userId) {
        return $this->redis->hGet("user_passports", $userId);
    }

    public function isValidPassword($username, $password) {
        return $this->compareHashes($this->redis->hGet("users", $username), $this->hashPassword($password));
    }

    public function getInfo($userId) {
        return $this->redis->hGet('infos', $userId);
    }

    public function setInfo($userId, $info) {
        return $this->redis->hSet('infos', $userId, $info);
    }

}