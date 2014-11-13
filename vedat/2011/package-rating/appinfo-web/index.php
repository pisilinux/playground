<?php

require_once('class.packimage.php');
require_once('class.appinfo.php');
require_once('class.database.php');

if (!isset($_GET['p'])) {
    echo 'Appinfo server, up and running.';
    exit();
}

$p = $_GET['p'];
$db = new Database();

if (isset($_GET['k'])) {
    $k = $_GET['k'];
    if (!$db->checkKey($k)) {
        unset($k);
    }
}

if (isset($_GET['s']) && isset($k)) {
    $s = $db->limitScore((float) $_GET['s']);
    $s = $db->processScore($p, $s);
    echo json_encode(array('p' => $p, 'score' => $s));
    exit();
} else {
    $s = $db->getScore($p);
}

$messages = array(
    'not_logged_in' => array(
        'class' => 'warning',
        'text' => 'You need to login before voting. Click <a href="#login">here</a> to login.'
    ),
    'invalid_key' => array(
        'class' => 'error',
        'text' => 'Your account could not be activated. Click <a href="#login">here</a> to re-activate.'
    ),
    'vote_saved' => array(
        'class' => 'success',
        'text' => 'Your vote has been saved. Thank you!'
    ),
    'already_voted' => array(
        'class' => 'information',
        'text' => 'You\\\'ve voted for this package.'
    ),
    'vote_changed' => array(
        'class' => 'success',
        'text' => 'Your vote has been changed.'
    )
);

$voted = false;
if (isset($k)) {
    if ($db->hasVoted($p)) {
        $voted = true;
        $status = 'vote_changed';
    } else {
        $status = 'vote_saved';
    }
} else {
    if (isset($_GET['k'])) {
        $status = 'invalid_key';
    } else {
        $status = 'not_logged_in';
    }
}

$pi = new PackImage($p);

?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
<head>
<meta http-equiv="Content-type" content="text/html; charset=utf-8" />
<meta http-equiv="Content-language" content="en" />
<link href="min/?g=css" rel="stylesheet" type="text/css" />
<script type="text/javascript">
var pack = '<?php echo $p; ?>';
var score = '<?php echo $s; ?>';
<?php

if (isset($k)) {
    printf("var key='%s';\n", $k);
?>
function raty_click(score, evt) {
    $.getJSON('', { p: pack, k: key, s: score }, function(json) {
        $.fn.raty.start(json.score, '.rating');
        <?php printf("showMessage('%s', '%s');\n", $messages[$status]['class'], $messages[$status]['text']); ?>
    });
}
<?php

} else {
    printf("function raty_click() {
    showMessage('%s', '%s');
}
", $messages[$status]['class'], $messages[$status]['text']);
}

?>
</script>
<script type="text/javascript" src="min/?g=js"></script>
<title>AppInfo Server</title>
</head>
<body>
<div class="container">
    <div class="gallery">
        <div class="image"><?php echo ($pi->exists()) ? $pi->show() : '<img src="img/back.png">'; ?></div>
    </div>
    <div class="info">
        <div id="title" class="title"></div>
        <div id="summary" class="summary"></div>
        <div id="description" class="description"></div>
        <div class="rating"></div>
    </div>
</div>
<div class="message"><div>
<?php if ($voted): ?>
<script type="text/javascript">
$(document).ready(function(){
    <?php printf("    showMessage('%s', '%s');\n", $messages['already_voted']['class'], $messages['already_voted']['text']); ?>
});
</script>
<?php endif; ?>
</body>
</html>
