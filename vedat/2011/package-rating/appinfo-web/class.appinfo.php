<?php

/**
 * Appinfo SQLite database class
 *
 * @author Onur Güzel <guzelmu@itu.edu.tr>
 * @copyright Copyright (C) 2011, TUBITAK/BILGEM
 * @license http://opensource.org/licenses/gpl-license.php GNU Public License
 * @package appinfo
 *
 */
class AppInfo {
    var $db = '';
    var $package = '';

    var $dbh = null;

    /**
     * Sets the package and DB file variables
     *
     * @param string $package
     * @param string $db
     */
    public function __construct($package, $db = null) {
        if (!is_null($db) && is_file($db)) {
            $this->db = $db;
        }
        if ($this->is_valid($package)) {
            $this->package = $package;
        }
    }

    /**
     * Closes database connection in case it is not closed
     */
    public function __destruct() {
        $this->dbh = null;
    }

    /**
     * Connects to database
     */
    public function connect() {
        if (is_null($this->dbh)) {
            try {
                $this->dbh = new PDO(sprintf('sqlite:%s', $this->db));
            } catch(PDOException $e) {
                echo $e->getMessage();
            }
        }
    }

    /**
     * Checks the package name with PiSi rules
     *
     * @param string $package
     *
     * @return bool
     */
    public function is_valid($package) {
        return preg_match('"^[A-Za-z0-9-_+]+$"', $package);
    }

    /**
     * Closes database connection
     */
    public function disconnect() {
        if (!is_null($this->dbh)) {
            $this->dbh = null;
        }
    }

    /**
     * Fetches package information from DB
     *
     * @return object|false
     */
    public function fetchInfo() {
        $this->connect();
        try {
            $sql = sprintf("SELECT * FROM packages WHERE name = %s", $this->dbh->quote($this->package));
            $r = $this->dbh->query($sql)->fetch(PDO::FETCH_OBJ);
        } catch(PDOException $e){
            echo $e->getMessage();
            $r = false;
        }
        $this->disconnect();
        return $r;
    }

    /**
     * Returns DB hash file
     *
     * @return string
     */
    public function hashFile() {
        return sprintf('%s.md5', $this->db);
    }

    /**
     * Updates DB hash file
     */
    public function updateHash() {
        if (is_writeable($this->hashFile())) {
            file_put_contents($this->hashFile(), md5_file($this->db));
        }
    }

    /**
     * Gets package score from DB
     *
     * @return float
     */
    public function getScore() {
        $score = 0;
        $row = $this->fetchInfo();
        if ($row !== false)
            if ($row->nose)
                $score = $row->score / $row->nose;
        return $score;
    }

    /**
     * Updates package score
     *
     * @param float $score
     *
     * @return float|false package score on success, false on failure
     */
    public function setScore($score) {
        try {
            $row = $this->fetchInfo();
            $this->connect();
            $sql = sprintf("UPDATE `packages` SET score = %.1f, nose = %d WHERE name = %s", $row->score + (float) $score, $row->nose + 1, $this->dbh->quote($this->package));
            $this->dbh->exec($sql);
            $this->disconnect();
            $this->updateHash();
            return $this->getScore();
        } catch(PDOException $e){
            echo $e->getMessage();
            $r = false;
        }
        $this->disconnect();
        return $r;
    }
}

?>
