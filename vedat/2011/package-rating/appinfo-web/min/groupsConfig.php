<?php
/**
 * Groups configuration for default Minify implementation
 * @package Minify
 */

/** 
 * You may wish to use the Minify URI Builder app to suggest
 * changes. http://yourdomain/min/builder/
 **/

function relative_path() {
    $rel = str_replace($_SERVER['DOCUMENT_ROOT'], null, str_replace(basename(dirname(__FILE__)), null, dirname(__FILE__)));
    return (preg_match('/^\//', $rel)) ? substr($rel, 1, strlen($rel)) : $rel;
}

$groupsConfig = array(
    'js' => array('//js/jquery.min.js', '//js/jquery.raty.min.js', '//js/effect.js'),
    'css' => array('//style.css')

    // custom source example
    /*'js2' => array(
        dirname(__FILE__) . '/../min_unit_tests/_test_files/js/before.js',
        // do NOT process this file
        new Minify_Source(array(
            'filepath' => dirname(__FILE__) . '/../min_unit_tests/_test_files/js/before.js',
            'minifier' => create_function('$a', 'return $a;')
        ))
    ),//*/

    /*'js3' => array(
        dirname(__FILE__) . '/../min_unit_tests/_test_files/js/before.js',
        // do NOT process this file
        new Minify_Source(array(
            'filepath' => dirname(__FILE__) . '/../min_unit_tests/_test_files/js/before.js',
            'minifier' => array('Minify_Packer', 'minify')
        ))
    ),//*/
);

foreach ($groupsConfig as $key => $files) {
    foreach ($files as $i => $file) {
        $groupsConfig[$key][$i] = str_replace('//', '//'.relative_path(), $file);
    }
}

return $groupsConfig;
