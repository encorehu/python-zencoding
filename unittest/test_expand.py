'''
Created on Jun 19, 2009

@author: sergey
'''
import unittest

from zencoding import zen_core as zen

#zen.update_settings(stparser.get_settings())

def expandAbbr(abbr, doc_type='html', profile_name='plain'):
	return zen.expand_abbreviation(abbr, doc_type, profile_name)

def extractAbbr(line):
	return zen.find_abbr_in_line(line, len(line))[0]

class Test(unittest.TestCase):

	def testPlusOperator(self):
		self.assertEqual('<p></p><p></p>', expandAbbr('p+p'))
		self.assertEqual('<p></p><p></p>', expandAbbr('p+P'))
		self.assertEqual('<p class="name"></p><p></p><p></p>', expandAbbr('p.name+p+p'))

	def testChildOperator(self):
		self.assertEqual('<p><em></em></p>', expandAbbr('p>em'))
		self.assertEqual('<p class="hello"><em class="world"><span></span></em></p>', expandAbbr('p.hello>em.world>span'))

	def testAttributes(self):
		self.assertEqual('<p class="name"></p>', expandAbbr('p.name'))
		self.assertEqual('<p class="one two three"></p>', expandAbbr('p.one.two.three'))
		self.assertEqual('<p class="one-two three"></p>', expandAbbr('p.one-two.three'))
		self.assertEqual('<p class="one two-three"></p>', expandAbbr('p.one.two-three'))
		self.assertEqual('<p class="one_two-three"></p>', expandAbbr('p.one_two-three'))
		self.assertEqual('<p id="myid"></p>', expandAbbr('p#myid'))
		self.assertEqual('<p id="myid" class="name_with-dash32 otherclass"></p>', expandAbbr('p#myid.name_with-dash32.otherclass'))
		self.assertEqual('<span class="one two three"></span>', expandAbbr('span.one.two.three'))

	def testExpandos(self):
		self.assertEqual('<dl><dt></dt><dd></dd></dl>', expandAbbr('dl+'))
		self.assertEqual('<table><tr><td></td></tr></table>', expandAbbr('table+'))
		self.assertEqual('<div></div><div><dl><dt></dt><dd></dd></dl></div>', expandAbbr('div+div>dl+'))

	def testCounters(self):
		self.assertEqual('<ul id="nav"><li class="item1"></li><li class="item2"></li><li class="item3"></li></ul>', expandAbbr('ul#nav>li.item$*3'))

	def testShortTags(self):
		self.assertEqual('<blockquote><p></p></blockquote>', expandAbbr('bq>p'))

	def testTagMatch(self):
		self.assertEqual('bq>p', extractAbbr('<div>bq>p'))
		self.assertEqual('bq>p', extractAbbr('<div class="hello" id="world">bq>p'))
		self.assertEqual('bq>p', extractAbbr('<div some:extention="value">bq>p'))

	def testMiscPatters(self):
		self.assertEqual('<script type="text/javascript"></script>', expandAbbr('script'))
		self.assertEqual('<script type="text/javascript" src=""></script>', expandAbbr('script:src'))
		self.assertEqual('<img src="" alt="" />', expandAbbr('img'))
		self.assertEqual('<input type="checkbox" name="" id="" />', expandAbbr('input:c'))
		self.assertEqual('<some:elem></some:elem>', expandAbbr('some:elem'))
		self.assertEqual('<li id="id1" class="class1"></li><li id="id2" class="class2"></li><li id="id3" class="class3"></li>', expandAbbr('li#id$.class$*3'))
		self.assertEqual('<select name="" id="test"></select>', expandAbbr('select#test'));

	def testXSL(self):
		self.assertEqual('<xsl:template match="" mode=""></xsl:template>', expandAbbr('tmatch', 'xsl'))
		self.assertEqual('<xsl:choose><xsl:when test=""></xsl:when><xsl:otherwise></xsl:otherwise></xsl:choose>', expandAbbr('choose+', 'xsl'))
		self.assertEqual('<xsl:variable><div></div><p></p></xsl:variable>', expandAbbr('xsl:variable>div+p', 'xsl'))
		self.assertEqual('<xsl:variable name=""><div></div><p></p></xsl:variable>', expandAbbr('var>div+p', 'xsl'))
		self.assertEqual('<xsl:apply-templates select="" mode="" />', expandAbbr('ap', 'xsl'));
		self.assertEqual('<xsl:apply-templates select="" mode=""><xsl:with-param name="" select="" /><xsl:with-param name="" select="" /></xsl:apply-templates>', expandAbbr('ap>wp*2', 'xsl'));

	def testCSS(self):
		self.assertEqual('@import url(|);', expandAbbr('@i', 'css'))
		self.assertEqual('!important', expandAbbr('!', 'css'))
		self.assertEqual('position:static;', expandAbbr('pos:s', 'css'))
		self.assertEqual('text-indent:-9999px;', expandAbbr('ti:-', 'css'))
		self.assertEqual('border-bottom:1px solid #000;', expandAbbr('bdb+', 'css'))

	def testInheritance(self):
		self.assertEqual('<a href=""></a>', expandAbbr('a', 'xsl'))

	def testNonExistedTypes(self):
		self.assertEqual('<a></a>', expandAbbr('a', 'foo'))
		self.assertEqual('<bq><p></p></bq>', expandAbbr('bq>p', 'foo'))

	def testTagHit(self):
		self.assertEqual(True, zen.is_inside_tag('hello<div>world', 7))
		self.assertEqual(True, zen.is_inside_tag('hello<br />world', 7))
		self.assertEqual(True, zen.is_inside_tag('hello</p>world', 7))
		self.assertEqual(False, zen.is_inside_tag('hello<div>world', 10))
		self.assertEqual(False, zen.is_inside_tag('hello<div>world', 1))

	def testFormatting(self):
		self.assertEqual('<blockquote>\n\t<p>|</p>\n</blockquote>', expandAbbr('bq>p', 'html', 'xhtml'));
		self.assertEqual('<blockquote>|</blockquote>\n<p>|</p>', expandAbbr('bq+p', 'html', 'xhtml'));
		self.assertEqual('<img src="|" alt="|" />\n<p>|</p>', expandAbbr('img+p', 'html', 'xhtml'));
		self.assertEqual('<xsl:variable name="|" select="|"/>', expandAbbr('vare', 'xsl', 'xml'));
		self.assertEqual('<xsl:variable name="|" select="|"/>\n<p>\n\t|\n</p>', expandAbbr('vare+p', 'xsl', 'xml'));

if __name__ == "__main__":
	#import sys;sys.argv = ['', 'Test.testAbbreviations']
	unittest.main()