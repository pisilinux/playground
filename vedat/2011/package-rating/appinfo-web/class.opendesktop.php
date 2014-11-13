<?php

/**
 * Özgürlükİçin Package Screenshots class
 *
 * @author Onur Güzel <guzelmu@itu.edu.tr>
 * @copyright Copyright (C) 2011, TUBITAK/BILGEM
 * @license http://opensource.org/licenses/gpl-license.php GNU Public License
 * @package appinfo
 */
class OpenDesktop {
    var $api_uri = 'http://api.opendesktop.org';

    /**
     * Calls API method
     *
     * @access private
     *
     * @param string $uri
     * @param array $post
     *
     * @return SimpleXMLElement
     */
    private function fetch($uri, $post = null) {
        $uri = $this->api_uri . $uri;
        $ch = curl_init();
        curl_setopt($ch, CURLOPT_URL, $uri);
        if (!is_null($post)) {
            curl_setopt($ch, CURLOPT_POST, 1);
            curl_setopt($ch, CURLOPT_POSTFIELDS, $post);
        }
        curl_setopt($ch, CURLOPT_HEADER, 0);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
        curl_setopt($ch, CURLOPT_TIMEOUT, 10);
        $output = curl_exec($ch);
        curl_close($ch);
        //TODO:Check if error?
        return simplexml_load_string($output);
    }

    /**
     * Checks user login information
     *
     * @param string $username
     * @param string $password
     *
     * @return object
     */
    public function PersonCheck($username, $password) {
        $xml = $this->fetch('/v1/person/check', array('login' => $username, 'password' => $password));
        return (object) array(
            'statuscode' => (int) $xml->meta->statuscode,
            'personid' => (string) $xml->data->person->personid
        );
    }

    /**
     * Registers a new user
     *
     * @param string $username
     * @param string $password
     * @param string $name
     * @param string $lastname
     * @param string $email
     */
    public function PersonAdd($username, $password, $name, $lastname, $email) {
        $xml = $this->fetch('/v1/person/add', array('login' => $username, 'password' => $password, 'firstname' => $name, 'lastname' => $lastname, 'email' => $email));
        return (int) $xml->meta->statuscode;
    }
}

?>
