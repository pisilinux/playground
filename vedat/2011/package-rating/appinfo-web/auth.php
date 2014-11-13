<?php

if (!empty($_POST['username']) && !empty($_POST['password'])) {
    require_once('class.database.php');

    $db = new Database();
    $chk['key'] = $db->checkLogin($_POST['username'], $_POST['password']);
    $chk['statuscode'] = ($chk['key']) ? 100 : 102;
    print json_encode($chk);
} else {
    print json_encode(array('statuscode' => 101));
}

?>
