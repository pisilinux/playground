<?php

/**
 * Appinfo MySQL database class
 *
 * @author Onur Güzel <guzelmu@itu.edu.tr>
 * @copyright Copyright (C) 2011, TUBITAK/BILGEM
 * @license http://opensource.org/licenses/gpl-license.php GNU Public License
 * @package appinfo
 */
class Database {
    private $db_host = 'localhost';
    private $db_user = 'guzelmu_appinfo';
    private $db_pass = 'appinfo';
    private $db_base = 'guzelmu_appinfo';

    private $dbh = null;

    private $id = null;
    private $username = null;
    private $key = null;

    /**
     * Connects to database
     *
     * @param array $db_info
     */
    public function __construct($db_info = null) {
        // Database config can be overwritten on construction.
        if (!is_null($db_info) && is_array($db_info)) {
            foreach ($db_info as $k => $v) {
                if (inarray($k, array('db_host', 'db_user', 'db_pass', 'db_base'))) {
                    $this->$k = $v;
                }
            }
        }
        try {
            $this->dbh = new PDO(sprintf('mysql:host=%s;dbname=%s', $this->db_host, $this->db_base), $this->db_user, $this->db_pass);
            $this->dbh->setAttribute(PDO::MYSQL_ATTR_USE_BUFFERED_QUERY, true);
        } catch(PDOException $e) {
            echo $e->getMessage();
        }
    }

    /**
     * Closes database connection
     */
    public function __destruct() {
        $this->dbh = null;
    }

    /**
     * Checks if the key exists in DB
     *
     * @param string $key
     *
     * @return bool
     */
    public function checkKey($key) {
        $this->key = $key;
        if ($this->keyExists()) {
            $this->username = $this->getInfo('username', 'key');
            $this->id = $this->getID();
            return true;
        } else {
            $this->key = null;
            return false;
        }
    }

    /**
     * Checks login info over OpenDesktop.org Public API
     *
     * @param string $username
     * @param string $password
     *
     * @return string|false key hash on success, false on failure
     */
    public function checkLogin($username, $password) {
        require_once('class.opendesktop.php');
        $od = new OpenDesktop();
        $check = $od->PersonCheck($username, $password)->statuscode;
        switch ($check) {
            /*
             * OpenDesktop.org Status codes:
             * 100: Valid login
             * 101: Required fields cannot be blank
             * 102: Invalid login
             */
            case 100:
                $this->username = $username;
                if ($this->userExists()) {
                    if ($this->getKey() !== $this->createKey($password)) {
                        $this->processKey($password, 'update');
                    }
                } else {
                    $this->processKey($password);
                }
                $this->id = $this->getID();
                $this->key = $this->getKey();
                return $this->key;
                break;
            case 102:
                return false;
                break;
            default:
                return false;
                break;
        }
    }

    /**
     * Creates a hash string using username and password
     *
     * @access private
     *
     * @param string $password
     *
     * @return string key hash
     */
    private function createKey($password) {
        return sha1(sprintf('^%s:%s$', $this->username, $password));
    }

    /**
     * Retrieves info from database
     *
     * @access private
     *
     * @return string|false requested column data on success, false on failure
     */
    private function getInfo($column, $by = 'username') {
        if (in_array($by, array('id', 'username', 'key'))) {
            $q = $this->dbh->query(sprintf("SELECT `%s` FROM `users` WHERE `%s` = %s;", $column, $by, $this->dbh->quote($this->$by)));
            $r = $q->fetch(PDO::FETCH_ASSOC);
            $q->closeCursor();
            return $r[$column];
        } else {
            return false;
        }
    }

    /**
     * Gets user ID from DB
     *
     * @return int user ID
     */
    public function getID($by = 'username') {
        return $this->getInfo('id', $by);
    }

    /**
     * Gets unique user key from DB
     *
     * @return string key hash
     */
    public function getKey($by = 'username') {
        return $this->getInfo('key', $by);
    }

    /**
     * Gets username from DB
     *
     * @param string $by
     *
     * @return string username
     */
    public function getUsername($by = 'key') {
        return $this->getInfo('username', $by);
    }

    public function getScore($package) {
        $sql = sprintf("SELECT SUM(score) as score, COUNT(score) as count FROM `ratings` WHERE `package` = %s;", $this->dbh->quote($package));
        $q = $this->dbh->query($sql);
        $r = $q->fetch(PDO::FETCH_ASSOC);
        $q->closeCursor();
        return ($r['score']) ? $r['score']/$r['count'] : 0;
    }

    public function hasVoted($package) {
        $sql = sprintf("SELECT id FROM `ratings` WHERE `user_id` = %d AND `package` = %s;", $this->id, $this->dbh->quote($package));
        $sqt = $this->dbh->prepare($sql);
        $sqt->execute();
        $r = $sqt->rowCount();
        $sqt->closeCursor();
        return $r;
    }

    /**
     * Searchs the DB with gien key
     *
     * @param string $key
     *
     * @return bool true if exists, false otherwise
     */
    public function keyExists() {
        return ($this->getID('key')) ? true : false;
    }

    public static function limitScore($score) {
        $min = 0.0;
        $max = 5.0;
        return min($max, max($min, $score));
    }

    /**
     * Inserts or updates user information
     *
     * @access private
     *
     * @param string $password
     * @param string $action
     *
     * @return string|false key hash on success, false on failure
     */
    private function processKey($password, $action = 'insert') {
        $key = $this->createKey($password);
        switch ($action) {
            case 'insert':
                $sql = sprintf("INSERT INTO `users` (`username`, `key`) VALUES (%s, %s);", $this->dbh->quote($this->username), $this->dbh->quote($key));
                break;
            case 'update':
                $sql = sprintf("UPDATE `users` SET `key` = %2$s WHERE `username` = %1$s;", $this->dbh->quote($this->username), $this->dbh->quote($key));
                break;
            default:
                return false;
        }
        return ($this->dbh->exec($sql)) ? $key : false;
    }

    /**
     * Inserts or updates user's vote on package
     *
     * @param string $package
     * @param float $score
     *
     * @return string|false key hash on success, false on failure
     */
    public function processScore($package, $score) {
        $score = $this->limitScore($score);
        $action = ($this->hasVoted($package)) ? 'update' : 'insert';
        switch ($action) {
            case 'insert':
                $sql = sprintf("INSERT INTO `ratings` (`user_id`, `package`, `score`) VALUES (%d, %s, %.1f);", $this->id, $this->dbh->quote($package), $score);
                break;
            case 'update':
                $sql = sprintf('UPDATE `ratings` SET `score` = %3$.1f WHERE `user_id` = %1$d AND `package` = %2$s;', $this->id, $this->dbh->quote($package), $score);
                break;
            default:
                return false;
        }
        return ($this->dbh->exec($sql)) ? $this->getScore($package) : false;
    }

    /**
     * Searchs the DB for given username
     *
     * @return bool
     */
    public function userExists() {
        return ($this->getID()) ? true : false;
    }
}

?>
