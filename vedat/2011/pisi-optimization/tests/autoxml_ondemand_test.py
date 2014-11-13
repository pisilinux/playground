# -*- coding: utf-8 -*

'''

test0 -> correct xml

test1 -> pisi.source.name not exist
test2 -> pisi.source.packager not exist
test3 -> pisi.source.packager.name not exist
test4 -> history not exist

'''

import pisi
import sys

tests = [
    (str, 'source'),
    (None, 'source.name'),
    (str, 'source.packager'),
    (None, 'source.packager.name'),
    (str, 'package')
    ]

def autoxml_test(xml_file, use_ondemand):
    values = {}
    errors = set()
    error_types = {}

    for i in xrange(len(tests)):
        try:
            a = pisi.metadata.MetaData()
            a.read(xml_file, use_ondemand=use_ondemand)
        except Exception, e:
            error_types[-1] = e.args
            for arg in e.args:
                if arg.find(xml_file) < 0:
                    errors.add(arg)
            continue

        test_function, test_attr = tests[i]

        try:
            y = a
            for s in test_attr.split('.'):
                if len(s) > 0:
                    y = getattr(y, s)

            if test_function:
                values[i] = test_function(y)
            else:
                values[i] = y

        except Exception, e:
            errors = errors.union(e.args)
            error_types[i] = e.args

    return values, errors, error_types

def compare_tests(xml_file):
    '''
    compare tests with use_ondemand and without use_ondemand
    '''

    a_values, a_errors, a_error_types = autoxml_test(xml_file, False)
    b_values, b_errors, b_error_types = autoxml_test(xml_file, True)

    v = a_values==b_values
    e = a_errors==b_errors
    error_count = len(a_errors) + len(b_errors)
    if error_count == 0:
        print "a_values == b_values: %s" % (a_values==b_values)
    print "a_errors == b_errors: %s" % (a_errors==b_errors)
    print "len(a_errors):", len(a_errors)
    print "len(b_errors):", len(b_errors)

    if not e:
        print "\na diff b: "
        print a_errors.difference(b_errors)
        print "\nb diff a: "
        print b_errors.difference(a_errors)

        print "\na: "
        print a_error_types
        print "\nb: "
        print b_error_types
    elif not v and error_count == 0:
        print a_values
        print "\n"
        print b_values

stack = ""
printValues = False

def compare_recursive(a, b):
    global stack
    if isinstance(a, list):
        for i in xrange(len(a)):
            stack += '[%s]' % i
            assert(len(a) == len(b))
            # print stack
            compare_recursive(a[i], b[i])
            stack = stack[:stack.rfind('[')]

    elif isinstance(a, str):
        assert str(a) == str(b)
        if printValues:
            print "%s = %s" % (stack, a)

    elif hasattr(a, '__metaclass__') and  a.__metaclass__ == pisi.pxml.autoxml.autoxml:
        for attr in a.__dict__.keys():
            if attr in ('use_ondemand', 'ondemand_dict'):
                continue

            stack += "."+attr

            s_b = set(b.__dict__.keys()).union(b.ondemand_dict.keys())
            assert set(a.__dict__.keys()).difference(s_b) == set()
            # print stack

            ai = getattr(a, attr)
            bi = getattr(b, attr)

            compare_recursive(ai, bi)
            stack = stack[:stack.rfind('.')]

    elif a == None:
        assert a == b
        if printValues:
            print "%s = None" % stack

    elif type(a) in (long, int):
        assert a == b
        if printValues:
            print "%s = %s" % (stack, a)

    elif type(a) in pisi.specfile.__dict__.values():
        assert str(a) == str(b)

    elif type(a) == pisi.pxml.autoxml.LocalText:
        assert a == b

    elif type(a) == unicode:
        assert a == b

    else:
        print "unexpected type: %s" % type(a)
        print stack
        exit()

def compare_full(xml_file, compare_type):
    '''
    compare all attributes with use_ondemand and without use_ondemand
    '''

    a = compare_type()
    b = compare_type()

    a.read(xml_file, use_ondemand=False)
    b.read(xml_file, use_ondemand=True)

    compare_recursive(a, b)

if __name__ == '__main__':
    test_files = []
    for i in range(5):
        test_files.append('test_xml/test%s.xml' % i)

    # parse args
    # TODO: ---
    arg_compare = False
    arg_compare_type = 'metadata'
    if len(sys.argv)==4 and sys.argv[1] == 'compare':
        arg_compare = True
        arg_compare_type = sys.argv[2]
        arg_compare_file = sys.argv[3]
    #

    if arg_compare_type == None or arg_compare_type == 'metadata':
        compare_type = pisi.metadata.MetaData
    elif arg_compare_type == 'index':
        compare_type = pisi.index.Index
    else:
        print "unexpected compare type: %s" % arg_compare_type
        exit()


    if arg_compare:
        compare_full(arg_compare_file, compare_type)
        print "compare all attributes ok\n"
    else:
        for test_file in test_files:
            print test_file
            compare_tests(test_file)
            print ""
    
