<?php

/**
 * Özgürlükİçin Package Screenshots class
 *
 * @author Onur Güzel <guzelmu@itu.edu.tr>
 * @copyright Copyright (C) 2011, TUBITAK/BILGEM
 * @license http://opensource.org/licenses/gpl-license.php GNU Public License
 * @package appinfo
 */
class PackImage {
    var $package = null;
    var $image_root = 'http://www.ozgurlukicin.com/tema/paket-goruntuleri';

    /**
     * Sets the package variable
     *
     * @param string $package
     */
    public function __construct($package) {
        $this->package = $package;
    }

    /**
     * Fetches given URI
     *
     * @access private
     *
     * @param string $uri
     * @return string|false page content on success, false on failure
     */
    private function getContents($uri) {
        $ch = curl_init();
        curl_setopt($ch, CURLOPT_URL, $uri);
        curl_setopt($ch, CURLOPT_HEADER, 0);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
        curl_setopt($ch, CURLOPT_TIMEOUT, 10);
        $output = curl_exec($ch);
        $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
        curl_close($ch);

        // List of HTTP status codes: http://en.wikipedia.org/wiki/List_of_HTTP_status_codes
        return ($httpCode == 200) ? $output : false;
    }

    /**
     * Check if a screenshot exists for package
     *
     * @return bool true if exists, false otherwise
     */
    public function exists() {
        $page = sprintf('%s/exists/%s/', $this->image_root, $this->package);

        return ($this->getContents($page) == 'True') ? True : False;
    }

    /**
     * Gives the image URL
     *
     * @param string $size
     * @return string image url
     */
    public function imageLink($size) {
        # Özgürlükİçin uses Turkish in URLs.
        # kucuk => small
        # buyuk => large
        # I apologize for inconvenience
        return sprintf('%s/ontanimli/%s/%s/', $this->image_root, (in_array($size, array('kucuk', 'buyuk'))) ? $size : 'kucuk', $this->package);
    }

    /**
     * Show package screenshot, with link to bigger image
     */
    public function show() {
        printf('<a href="%s"><img src="%s" alt="%s" /></a>', $this->imageLink('buyuk'), $this->imageLink('kucuk'), $this->package);
    }
}

?>
